from toolshed import toolshed_context
from toolshed import PICO_COLORS, DEFAULT_PICO8_FONT_SIZE, PICO8_DIMS
from toolshed.ttf_printer import init_printers

# setup ToolshedContext object
toolshed_context.appname = '"PROJECT_APP_NAME"'
toolshed_context.title = '"PROJECT_TITLE"'
toolshed_context.root_dir_name = '"PROJECT_ROOT_NAME"'

printer_params = {
    'regular': {
        'font': {
            'filename': 'assets/PICO-8.ttf',
            'size': DEFAULT_PICO8_FONT_SIZE
        },
        'color': PICO_COLORS.DarkBlue.value
    }
}
printers = init_printers(printer_params)

WIDTH, HEIGHT = PICO8_DIMS
