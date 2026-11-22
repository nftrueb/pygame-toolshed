import sys
import os
import subprocess
import stat
from pathlib import Path
from toolshed import logger
from toolshed.cli import CLI
from toolshed.text import bold

def cp_file(src: Path, dest: Path): 
    logger.debug(f'Copying file...\nSrc: {src}\nDest: {dest}')
    with open(src, 'r') as src_file: 
        with open(dest, 'w') as dest_file: 
            dest_file.write(src_file.read())

def replace_patterns_in_file(file: Path, patterns): 
    fixed = file.read_text()
    unmatched_patterns = []
    for tup in patterns: 
        pattern, replace = tup
        idx = fixed.find(pattern)
        if idx != -1: 
            fixed = fixed[:idx] + replace + fixed[idx + len(pattern):] 
        else: 
            unmatched_patterns.append(pattern)

    # write fixed text to file or log error
    if len(unmatched_patterns) == 0: 
        file.write_text(fixed)
    else: 
        logger.error(
            f'Failed to fix the following patterns in {file.name}: {' '.join(unmatched_patterns)}'
        )
    logger.info(f'Finished generating {file.name}')

def validate_dirs(dirs): 
    missing_dirs = [ str(dir) for dir in dirs.values() if not dir.exists()]
    if len(missing_dirs) > 0: 
        logger.error(f'Missing necessary directory: {'\n  - '.join(missing_dirs)}')
        sys.exit()

def make_dirs(dirs, keys): 
    for key in keys: 
        path = dirs[key]
        if not path.exists(): 
            path.mkdir()
        else: 
            logger.info(f'Directory already exists: {path}')

def build(flags): 
    project_name = flags['--name']
    title = flags['--title']
    toolshed_dir = flags['--toolshed']

    # directory vars
    dirs = {}
    dirs['root'] = Path(flags['--root']).resolve()
    dirs['toolshed'] = Path(toolshed_dir).resolve()
    dirs['toolshed-builder'] = Path(f'{__file__}/../../../').resolve()
    dirs['resources'] = Path(dirs['toolshed-builder'] / 'resources')
    dirs['project'] = Path(dirs['root'] / flags['--name'])
    dirs['output'] = Path(dirs['project'] / 'output')
    dirs['scripts'] = Path(dirs['project'] / 'scripts')
    dirs['assets'] = Path(dirs['project'] / 'assets')
    dirs['web'] = Path(dirs['project'] / 'web')

    # clean up old project files 
    if dirs['project'].exists(): 
        logger.info('Existing project with same name found ... cleaning up project files now')
        clean(flags)

    # create new project dirs
    make_dirs(dirs, ['project', 'output', 'scripts', 'assets', 'web'])
    validate_dirs(dirs)

    # root directory must exist otherwise we cannot continue...
    # protects against accidentally creating a new path with a typo
    if not dirs['root'].exists(): 
        logger.error(f'Invalid --root provided: {dirs['root']}')
        sys.exit()

    # prompt for confirmation before continuing
    prompt = 'Create new project with the following name and root directory?\n'
    prompt += f'Root Directory: {dirs['root']}\n'
    prompt += f'Project Name  : {project_name}\n'
    prompt += f'(y/n) >>> '
    if input(prompt).strip().lower() != 'y': 
        logger.error('Confirmation required before creating project')
        sys.exit()

    # build dir at root
    logger.debug(f'Building project dir at path: {bold(dirs['project'])}')
    if not dirs['project'].exists(): 
        os.mkdir(dirs['project'])
    else: 
        logger.info('Project directory already exists ...')

    # uv init --name {name} --package
    pyproject_file = Path(dirs['project'] / 'pyproject.toml')
    if not pyproject_file.exists(): 
        uv_init_comm = f'uv init --name {project_name} --package --directory {dirs['project']}/'
        logger.info(f'Running uv init command\n$ {uv_init_comm}')
        subprocess.run(uv_init_comm.split(' '), capture_output=True, text=True)
    else: 
        logger.info('uv init has already been run ...')

    # generate pyproject.toml
    replace_patterns_in_file(
        file = pyproject_file, 
        patterns = [
            (f'"{project_name}:main"', f'"{project_name}.main:main"')
        ]
    )

    # generate main.py
    main_file = Path(dirs['project'] / f'src/{project_name}/main.py')
    cp_file(
        src=(Path(__file__) / f'../../../resources/main-template.py').resolve().absolute(), 
        dest=main_file
    )
    replace_patterns_in_file(
        file = main_file, 
        patterns = [
            ('{{PROJECT_APP_NAME}}', project_name)
        ]
    )

    # generate constants.py
    constants_file = Path(dirs['project'] / f'src/{project_name}/constants.py')
    cp_file(
        src=(Path(__file__) / f'../../../resources/constants-template.py').resolve().absolute(), 
        dest=constants_file
    )
    replace_patterns_in_file(
        file = constants_file, 
        patterns = [ 
            ('{{PROJECT_APP_NAME}}', project_name),
            ('{{PROJECT_TITLE}}', title), 
            ('{{PROJECT_ROOT_NAME}}', f'{str(dirs['root'])}/') 
        ]
    )

    # add toolshed dependency
    uv_add_comm = f'uv add --directory {dirs['project']} --editable {dirs['toolshed']}'
    logger.info(f'Running uv add command:\n$ {uv_add_comm}')
    subprocess.run(uv_add_comm.split(' '))

    # add requirements.txt dependencies
    requirements_file = Path(dirs['toolshed'] / 'requirements.txt')
    uv_add_req_comm = f'uv add -r {requirements_file} --directory {dirs['project']}'
    logger.info(f'Running uv add command:\n$ {uv_add_req_comm}')
    subprocess.run(uv_add_req_comm.split(' '))

    # install tool to path
    uv_tool_install_comm = f'uv tool install --editable {dirs['project']}'
    logger.info(f'Running uv tool install command:\n$ {uv_tool_install_comm}')
    subprocess.run(uv_tool_install_comm.split(' '))

    # create output directory for output files from app and toolshed 
    dirs['output'] = Path(dirs['project'] / 'output')
    if not dirs['output'].exists(): 
        dirs['output'].mkdir()

    # create scripts directory
    dirs['scripts'] = Path(dirs['project'] / 'scripts')
    if not dirs['scripts'].exists():
        dirs['scripts'].mkdir() 

    # create assets directory
    dirs['assets'] = Path(dirs['project'] / 'assets')
    if not dirs['assets'].exists(): 
        dirs['assets'].mkdir()

    asset_files = [ 
        ('icon-generated.png', 'icon.png'), 
        ('icon-generated.icns', 'icon.icns'), 
        ('PICO-8.ttf', 'PICO-8.ttf')
    ]
    for tup in asset_files: 
        src_name, dest_name = tup
        with open(dirs['resources'] / src_name, 'rb') as src: 
            with open(dirs['project'] / 'assets' / dest_name, 'wb') as dest: 
                dest.write(src.read())

    web_main_file = Path(dirs['web'] / 'main.py')
    with open(dirs['resources'] / 'web_main.py', 'r') as src: 
        with open(web_main_file, 'w') as dest: 
            dest.write(src.read())
    replace_patterns_in_file(
        web_main_file, 
        patterns=[
            ('{{PROJECT_APP_NAME}}', project_name)
        ]
    )

    # add output (and other?) files to .gitignore
    gitignore_file = Path(dirs['project'] / '.gitignore')
    contents = gitignore_file.read_text()
    contents += '\n# Toolshed\n'
    contents += 'output/*'
    gitignore_file.write_text(contents)

    # add build script and update executable permissions
    build_script = Path(dirs['scripts'] / 'build.sh') 
    with open(dirs['resources'] / 'build.sh', 'r') as src: 
        with open(build_script, 'w') as dest:
            dest.write(src.read()) 
    replace_patterns_in_file(
        build_script, 
        patterns = [ 
            ('{{APPNAME}}', title),
            ('{{PROJECT_NAME}}', project_name), 
        ]
    )
    build_script.chmod(build_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # add build script for web and update executable permissions
    build_script = Path(dirs['scripts'] / 'build-web.sh')
    with open(dirs['resources'] / 'build-web.sh', 'r') as src: 
        with open(build_script, 'w') as dest:
            dest.write(src.read()) 
    replace_patterns_in_file(
        build_script, 
        patterns = [ 
            ('{{PROJECT_APP_NAME}}', project_name),
            ('{{PROJECT_TITLE}}', title)
        ]
    )
    build_script.chmod(build_script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # run build script that links shortcut on Desktop 
    os.chdir(dirs['project'])
    if not flags['--no-build']: 
        subprocess.run(['./scripts/build.sh']) 

    logger.info(f'Finished building new project: {project_name}')

def rec_remove_files_in_directory(curr_dir: Path): 
    dirs = []
    for file in curr_dir.iterdir(): 
        file = file.absolute()
        if file.is_file() or file.is_symlink(): 
            file.unlink()
        else: 
            dirs.append(file)

    if len(dirs) > 0: 
        for dir in dirs: 
            rec_remove_files_in_directory(dir)
    curr_dir.rmdir()

def clean(flags):  
    project_name = flags['--name']
    title = flags['--title']

    dirs = {}
    dirs['root'] = Path(flags['--root']) 
    dirs['project'] = Path(dirs['root'] / project_name)

    # clean out project dir recursively
    if dirs['project'].exists():
        logger.info(f'Removing project files from {dirs['project']} ...')
        rec_remove_files_in_directory(dirs['project'])
    else: 
        logger.info(f'Project files do not exist: {dirs['project']}')

    # remove .app from /Applications
    application_dir = Path(f'/Applications/{title}.app')
    if application_dir.exists():
        logger.info(f'Removing application files from {application_dir} ...')
        rec_remove_files_in_directory(application_dir)
    else: 
        logger.info(f'Application does not exist: {application_dir}')

    # unlink shortcut in Desktop 
    desktop_shortcut_path = Path.home() / Path(f'Desktop/{title}')
    if desktop_shortcut_path.is_symlink(): 
        logger.info('Unlinking Desktop shortcut ...')
        desktop_shortcut_path.unlink()
    else: 
        logger.info(f'Desktop shortcut is already unlinked: {desktop_shortcut_path}')

    # uv uninstall tool {project_name}
    uninstall_tool = True
    response = subprocess.run(['uv', 'tool', 'dir'], capture_output=True, text=True)
    if response.returncode == 0: 
        uv_tool_dir = Path(response.stdout.strip())
        if uv_tool_dir.exists(): 
            tools = [ tool for tool in uv_tool_dir.iterdir() ] 
            if project_name not in tools: 
                logger.info('Skipping uv tool uninstall')
                uninstall_tool = False
        else: 
            logger.error('Failed to get uv tools directory. Attempting to uninstall tool anyway') 
    else: 
        logger.error('Failed to get uv tools directory. Attempting to uninstall tool anyway')

    if uninstall_tool: 
        command = f'uv tool uninstall {project_name}'
        logger.info(f'Running uninstall command: \n$ {command}')
        subprocess.run(command.split(' '))

def init_cli() -> CLI: 
    return (
        CLI('toolshed-builder', 'CLI for building new Toolshed projects')
        .option(name='--name', description='name of project folder')
        .option(name='--root', description='path that project folder will be made in')
        .option(name='--title', description='title displayed in app window')
        .option(
            name='--clean', 
            is_flag=True,
            description='removes all lingering traces of the specified project', 
            required=False
        )
        .option(
            name='--no-build', 
            is_flag=True,
            description='skips building and creating a symlink on ~/Desktop',
            required=False
        )
        .option(name='--toolshed', description='directory of toolshed package')
    ) 

def main(): 
    cli = init_cli()
    flags = cli.parse()

    if flags['--clean']: 
        clean(flags)
    else: 
        build(flags)
