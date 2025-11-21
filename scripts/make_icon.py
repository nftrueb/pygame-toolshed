import sys
import pygame as pg 
from PIL import Image

def usage(): 
    print('./venv/bin/python scripts/make_icon.py [255 255 255]')

def main(): 
    if '--help' in sys.argv: 
        usage()
        sys.exit(0)

    # define color ... could be passed from user 
    c = (255,255,255)
    if len(sys.argv) == 4: 
        c = tuple([int(sys.argv[i]) for i in range(1,4)])
        print(f'[ INFO ] User provided color: {c}')

    # define new surface
    dim, pad, rad, icon_pad = 1024, 86, 228, 128
    surf = pg.Surface((dim, dim), pg.SRCALPHA)

    # draw corner circles
    pg.draw.circle(surf, c, (pad+rad,     pad+rad),     rad)
    pg.draw.circle(surf, c, (dim-pad-rad, pad+rad),     rad)
    pg.draw.circle(surf, c, (pad+rad,     dim-pad-rad), rad)
    pg.draw.circle(surf, c, (dim-pad-rad, dim-pad-rad), rad)

    # draw horizontal rect to connect cicles 
    x = pad 
    y = pad + rad 
    w = dim - pad - x 
    h = dim - pad - rad - y 
    pg.draw.rect(surf, c, (x,y,w,h))

    # draw vertical rect to connect cicles
    x = pad + rad
    y = pad
    w = dim - pad - rad - x 
    h = dim - pad - y 
    pg.draw.rect(surf, c, (x,y,w,h))

    # load 16x16 icon 
    pad, dim = 128, 768
    input_path = 'assets/icon.png'
    print(f'[ INFO ] Looking for input icon at path: {input_path}')
    try: 
        icon = pg.image.load(input_path)
    except Exception as e: 
        print(f'[ ERROR ] Failed to load image:\n{e}')
        sys.exit(1)

    # scale and blit icon 
    icon_scaled = pg.transform.scale(icon, (dim, dim))
    surf.blit(icon_scaled, (pad, pad))

    # save generated image
    try: 
        output_path = 'assets/icon-generated.png'
        pg.image.save(surf, output_path)
        print(f'[ INFO ] Saved image to path: {output_path}')
    except Exception as e: 
        print(f'[ ERROR ] Failed to save image:\n{e}')
        sys.exit(1)

    # convert generated image to .icns format
    try: 
        icns_path = output_path[:-4] + '.icns'
        with Image.open(output_path) as img: 
            img.save(icns_path)
        print(f'[ INFO ] Saved image to path: {icns_path}')
    except Exception as ex: 
        print(f'[ ERROR ] Failed to write .icns file')
        sys.exit(1)    

if __name__ == '__main__': 
    main() 