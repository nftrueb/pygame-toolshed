from toolshed import PICO_COLORS, DEFAULT_PICO8_FONT_SIZE, PICO8_DIMS
from toolshed.ttf_printer import ShadowDirection

WIDTH, HEIGHT = PICO8_DIMS
printer_params = {
    'regular': {
        'font': {
            'filename': 'assets/PICO-8.ttf', 
            'size': DEFAULT_PICO8_FONT_SIZE
        },
        'color': PICO_COLORS.DarkBlue.value
    }
}