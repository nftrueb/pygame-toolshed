import sys
from dataclasses import dataclass 
import pyperclip as clipboard
from toolshed import logger
from toolshed.text import bold

@dataclass
class Option: 
    name: str 
    value: str
    is_flag: bool
    description: str 
    required: bool

class CLI: 
    def __init__(self, name: str, description: str = '* no description provided *'): 
        self.name = name
        self.description = description
        self.options: dict[str: Option] = {}
        self.options['--help'] = Option(
            name='--help', 
            value=None, 
            is_flag=True, 
            description='print this message', 
            required=False
        )

    def __str__(self): 
        return f'Option()' 
    
    def print_sorted_options(self, options): 
        s = ''
        max_prefix_len = max([len(name) for name in self.options.keys()])
        for k in sorted(options): 
            opt = self.options[k]
            pad = ''.join([' ' for _ in range(max_prefix_len - len(k))])
            s += f'  {opt.name}{pad} -> {opt.description}\n'
        return s
        
    
    def usage(self): 
        s = f'DESCRIPTION: {self.description}\n'
        s += f'OPTIONS:\n'
        s += '(required)\n'
        s += self.print_sorted_options(
            [key for key in self.options.keys() if self.options[key].required ]
        )
        s += '\n(optional)\n'
        s += self.print_sorted_options(
            [key for key in self.options.keys() if not self.options[key].required ]
        )
        print(s)


    def option(self, 
            name: str, 
            is_flag: bool = False, 
            description: str = '* no description provided *',
            required: bool = True): 
        self.options[name] = (Option(name, None, is_flag, description, required))
        return self 
    
    def parse(self, args: list[str] = sys.argv[1:]): 
        flags = { name: None for name in self.options.keys() }

        idx = 0 
        while idx < len(args):
            opt = self.options[args[idx]]
            if opt.is_flag: 
                flags[opt.name] = True 
            else: 
                idx += 1 
                flags[opt.name] = args[idx]
            idx += 1

        if flags['--help']: 
            self.usage()
            sys.exit()

        missing_value_options = [ 
            key for key in self.options.keys() 
            if flags[key] is None and not self.options[key].is_flag and self.options[key].required
        ]

        missing_flag_options = [
            key for key in self.options.keys() 
            if flags[key] is None and self.options[key].is_flag and self.options[key].required
        ]

        if len(missing_value_options) + len(missing_flag_options) > 0: 
            print(f'Missing some arguments ... Enter them now')
            for key in missing_value_options: 
                flags[key] = input(f'{key} > ').strip()
            for key in missing_flag_options: 
                flags[key] = input(f'{key} (y/n) > ').strip().lower() == 'y'

            command = f'{self.name} '
            for key, value in flags.items(): 
                opt = self.options[key]
                if opt.is_flag and value: 
                    command += f'{key} '
                elif not opt.is_flag: 
                    command += f'{key} {value} '
            print(f'Copying complete command to clipboard:\n {bold(command)}\n')

        return flags
