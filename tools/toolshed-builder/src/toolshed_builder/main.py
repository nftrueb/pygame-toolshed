import sys
import os
import subprocess
from pathlib import Path
from toolshed import logger, toolshed_context
from toolshed.cli import CLI
from toolshed.text import bold

def init_cli() -> CLI: 
    return (
        CLI('CLI for building new Toolshed projects')
        .option(name='--name', description='name of project folder')
        .option(name='--root', description='path that project folder will be made in')
    ) 

def main(): 
    cli = init_cli()
    flags = cli.parse()

    root_dir = Path(flags['--root']) 
    project_dir = root_dir / flags['--name']
    if not root_dir.exists(): 
        logger.error(f'Invalid --root provided: {root_dir}')
        sys.exit()

    # build dir at root
    logger.debug(f'Building project dir at path: {bold(project_dir)}')
    if not project_dir.exists(): 
        os.mkdir(project_dir)
    else: 
        logger.info('Project directory already exists ...')

    # uv init --name {name} --package
    pyproject_file = project_dir / 'pyproject.toml'
    if not pyproject_file.exists(): 
        uv_init_comm = ' '.join(
            ['uv', 'init', '--name', flags['--name'], '--package', '--directory', str(project_dir) + '/']
        )
        subprocess.run(uv_init_comm.split(' '), capture_output=True, text=True)
    else: 
        logger.info('uv init has already been run ...')

    # sub package:main in pyproject.toml
    with open(pyproject_file, 'r') as f: 
        contents = f.read() 

    search_string = f'"{flags['--name']}:main"'
    idx = contents.find(search_string)
    fixed = contents[:idx] + f'"{flags['--name']}.main:main"' + contents[idx + len(search_string):]
    logger.debug(fixed)

    # gen main.py

    # uv add toolshed

    # uv tool install {name} --editable . 

