import sys
from dataclasses import dataclass 

@dataclass
class Option: 
    name: str 
    value: str
    is_flag: bool
    description: str 

class CLI: 
    def __init__(self, description: str = '* no description provided *'): 
        self.description = description
        self.options: dict[str: Option] = {}
        self.options['--help'] = Option('--help', None, is_flag=True, description='print this message')

    def __str__(self): 
        return f'Option()' 
    
    def usage(self): 
        s = f'DESCRIPTION: {self.description}\n'
        s += f'OPTIONS:\n'
        for k in sorted(self.options.keys()): 
            opt = self.options[k]
            s += f'  {opt.name} -> {opt.description}\n'
        print(s)


    def option(self, 
            name: str, 
            is_flag: bool = False, 
            description: str = '* no description provided *'): 
        self.options[name] = (Option(name, None, is_flag, description))
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

        return flags
