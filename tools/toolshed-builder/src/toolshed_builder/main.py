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
        .option(name='--title', description='title displayed in app window')
    ) 

def copy_template_file(src: Path, dest: Path): 
    logger.debug(f'Generating file with template: {str(src)}')
    logger.debug(f'Generating new file at: {str(dest)}')
    with open(src, 'r') as template_file: 
        with open(dest, 'w') as new_main_file: 
            new_main_file.write(template_file.read())

def replace_in_str(pattern: str, replace: str, contents: str): 
    idx = contents.find(pattern)
    fixed = contents[:idx] + replace + contents[idx + len(pattern):] if idx != -1 else '' 
    return (fixed, idx != -1)

def main(): 
    cli = init_cli()
    flags = cli.parse()

    root_dir = Path(flags['--root']) 
    project_name = flags['--name']
    project_dir = Path(root_dir / flags['--name'])
    title = flags['--title']
    if not root_dir.exists(): 
        logger.error(f'Invalid --root provided: {root_dir}')
        sys.exit()

    # prompt for confirmation before continuing
    prompt = 'Create new project with the following name and root directory?\n'
    prompt += f'Root Directory: {root_dir}\n'
    prompt += f'Project Name  : {project_name}\n'
    prompt += f'(y/n) >>> '
    if input(prompt).strip().lower() != 'y': 
        logger.error('Confirmation required before creating project')
        sys.exit()

    # build dir at root
    logger.debug(f'Building project dir at path: {bold(project_dir)}')
    if not project_dir.exists(): 
        os.mkdir(project_dir)
    else: 
        logger.info('Project directory already exists ...')

    # uv init --name {name} --package
    pyproject_file = Path(project_dir / 'pyproject.toml')
    if not pyproject_file.exists(): 
        uv_init_comm = f'uv init --name {project_name} --package --directory {project_dir}/'
        logger.info(f'Running uv init command\n$ {uv_init_comm}')
        subprocess.run(uv_init_comm.split(' '), capture_output=True, text=True)
    else: 
        logger.info('uv init has already been run ...')

    # sub package:main in pyproject.toml
    contents = pyproject_file.read_text()
    fixed, found = replace_in_str(
        pattern=f'"{project_name}:main"', 
        replace=f'"{project_name}.main:main"', 
        contents=contents
    )
    if found: 
        pyproject_file.write_text(fixed)
    else: 
        logger.info(f'Failed to find "{project_name}:main" in pyproject.toml')

    # gen main.py
    main_file = Path(project_dir / f'src/{project_name}/main.py')
    copy_template_file(
        src=(Path(__file__) / f'../../../resources/main-template.py').resolve().absolute(), 
        dest=main_file
    )
    fixed = main_file.read_text()
    not_fixed = []
    patterns = [ ('"PROJECT_APP_NAME"', project_name)]
    for tup in patterns: 
        pattern, replace = tup
        logger.debug(f'Replacing {pattern}')
        fixed, found = replace_in_str(pattern, replace, fixed)
        if not found: 
            not_fixed.append(pattern)
            break
    if len(not_fixed) == 0: 
        main_file.write_text(fixed)
    else: 
        logger.error(f'Failed to fix the following patterns in main.py: {' '.join(not_fixed)}')
    logger.info('Finished generating main.py')

    # gen constants.py
    constants_file = Path(project_dir / f'src/{project_name}/constants.py')
    copy_template_file(
        src=(Path(__file__) / f'../../../resources/constants-template.py').resolve().absolute(), 
        dest=constants_file
    )

    # replace appname, title, and root name in constants file
    fixed = constants_file.read_text()
    not_fixed = []
    patterns = [ 
        ('"PROJECT_APP_NAME"', project_name),
        ('"PROJECT_TITLE"', title), 
        ('"PROJECT_ROOT_NAME"', f'{str(root_dir)}/') 
    ]
    for tup in patterns: 
        pattern, replace = tup
        logger.debug(f'Replacing {pattern}')
        fixed, found = replace_in_str(pattern, replace, fixed)
        if not found: 
            not_fixed.append(pattern)
            break
    if len(not_fixed) == 0: 
        constants_file.write_text(fixed)
    else: 
        logger.error(f'Failed to fix the following patterns in constants.py: {' '.join(not_fixed)}')
    logger.info('Finished generating constants.py')

    # add toolshed dependency
    toolshed_dir = Path('/Users/nicktrueb/Programming/toolshed')
    uv_add_comm = f'uv add --directory {project_dir} {toolshed_dir}'
    logger.info(f'Running uv add command:\n$ {uv_add_comm}')
    subprocess.run(uv_add_comm.split(' '))

    # add requirements.txt dependencies
    requirements_file = Path(toolshed_dir / 'requirements.txt')
    uv_add_req_comm = f'uv add -r {requirements_file} --directory {project_dir}'
    logger.info(f'Running uv add command:\n$ {uv_add_req_comm}')
    subprocess.run(uv_add_req_comm.split(' '))

    # install tool to path
    uv_tool_install_comm = f'uv tool install --editable {project_dir}'
    logger.info(f'Running uv tool install command:\n$ {uv_tool_install_comm}')
    subprocess.run(uv_tool_install_comm.split(' '))

    # create assets directory
    assets_dir = Path(project_dir / 'assets')
    if not assets_dir.exists(): 
        assets_dir.mkdir()

    asset_files = [ 
        ('icon-generated.png', 'icon.png'), 
        ('icon-generated.icns', 'icon.icns'), 
        ('PICO-8.ttf', 'PICO-8.ttf'), 
    ]
    for tup in asset_files: 
        src_name, dest_name = tup
    with open(toolshed_dir / 'tools/toolshed-builder/resources' / src_name, 'rb') as src: 
        with open(project_dir / 'assets' / dest_name, 'wb') as dest: 
            dest.write(src.read())


    output_dir = Path(project_dir / 'output')
    if not output_dir.exists(): 
        output_dir.mkdir()
