import pygame as pg

from toolshed.font import FontSpriteWriter, Dialogue
from toolshed.ui import UI, Node

WIDTH, HEIGHT = 320,180

# atlas offsets 
atlas_offsets = {
	'A_INC'  : (53, 0, 10, 10),
	'A_DEC'  : (43, 0, 10, 10),
	'A_BACK' : (0, 0, 43, 19), 

	'A_INC_INV' : (53, 10, 10, 10), 
	'A_DEC_INV' : (43, 10, 10, 10), 
	'A_BACK_INV': (0, 19, 43, 19), 
}

def get_window_scale(src, dest):
	return min(dest[0] // src[0], dest[1] // src[1])

def main():
	# initializing screen and scaling to size
	pg.init()
	display_info = pg.display.Info()
	scale = get_window_scale(
		(WIDTH, HEIGHT), 
		(display_info.current_w * .7, display_info.current_h)
	)
	screen = pg.display.set_mode((WIDTH*scale, HEIGHT*scale), pg.RESIZABLE)
	frame = pg.Surface((WIDTH, HEIGHT))
	clock = pg.time.Clock()
	pg.display.set_caption('UI Demo')

	# loading font sprites
	font_img = pg.image.load('assets/font.png').convert()
	font_writer = FontSpriteWriter(font_img)

	# load sprite assets 
	atlas = pg.image.load('assets/toolshed-atlas.png').convert()
	atlas.set_colorkey((255,0,255))
	inc_img = atlas.subsurface(atlas_offsets['A_INC'])
	inc_img_inv = atlas.subsurface(atlas_offsets['A_INC_INV'])
	dec_img = atlas.subsurface(atlas_offsets['A_DEC'])
	dec_img_inv = atlas.subsurface(atlas_offsets['A_DEC_INV'])
	back_img = atlas.subsurface(atlas_offsets['A_BACK'])
	back_img_inv = atlas.subsurface(atlas_offsets['A_BACK_INV'])

	# creating UIs for pause menu and game menu 
	button_w = WIDTH // 5 * 2
	button_h = HEIGHT // 10

	pause_ui = UI()
	pause_ui.insert(Node('Resume', pg.Rect(96, 36, button_w, button_h)))
	pause_ui.insert(Node('Options', pg.Rect(96, 72, button_w, button_h)))
	pause_ui.insert(Node('Quit', pg.Rect(96, 108, button_w, button_h)))

	game_ui = UI()
	w, h = inc_img.get_size()
	game_ui.insert(
		Node('Pause', pg.Rect(5, 5, w, h), img=inc_img, pressed_img=inc_img_inv)
	)

	# slider and increments
	options_ui = UI()
	w, h = back_img.get_size()
	options_ui.insert(
		Node('Back', pg.Rect(139, 144, w, h), img=back_img, pressed_img=back_img_inv)
	)
	w, h = inc_img.get_size()
	options_ui.insert(
		Node('Inc', pg.Rect(260, 67, w, h), img=inc_img, pressed_img=inc_img_inv)
	)
	w, h = dec_img.get_size()
	options_ui.insert(
		Node('Dec', pg.Rect(211, 67, w, h), img=dec_img, pressed_img=dec_img_inv)
	)

	value = 0

	running = True
	paused = True 
	options = False
	while running:
		# get mouse position at start of frame
		mx, my = pg.mouse.get_pos()
		mx //= scale 
		my //= scale 

		# set UI object based on current state
		ui = game_ui
		if paused: 
			ui = pause_ui
		if options: 
			ui = options_ui

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False

			elif event.type == pg.KEYUP: 
				if event.key == pg.K_SPACE: 
					paused = True

			elif event.type == pg.MOUSEBUTTONDOWN: 
				node = ui.get_node((mx, my))
				if node and isinstance(node, Node): 
					node.filled = not node.filled

			elif event.type == pg.MOUSEBUTTONUP:
				node = ui.get_node((mx, my))
				if node and isinstance(node, Node):
					node.filled = False
					# pause ui nodes
					if node.tag == 'Resume': 
						paused = False 

					if node.tag == 'Quit': 
						running = False 

					if node.tag == 'Options': 
						options = True 

					# game ui nodes
					if node.tag == 'Pause': 
						paused = True

					# options ui nodes
					if node.tag == 'Back': 
						options = False 

					if node.tag == 'Dec': 
						value = max(value-1, 0) 

					if node.tag == 'Inc': 
						value += 1 
		
		# clear new frame
		frame.fill((255,255,255))
		
		ui.draw(frame)

		if ui == pause_ui:
			x = WIDTH//2
			texts = {
				'Resume': 45, 
				'Options': 81, 
				'Quit': 117
			}
			for text, y_pos in texts.items(): 
				text_w, text_h = font_writer.get_size(text)
				dialogue = Dialogue(text, pg.Rect(x-text_w//2, y_pos-text_h//2, text_w, text_h))
				font_writer.render(frame, dialogue)

		if ui == options_ui: 
			text = str(value)
			w, h = font_writer.get_size(text)
			dialogue = Dialogue(text, (241 - w//2, 68, w, h))
			font_writer.render(frame, dialogue)

		# scale the frame 
		fw, fh = frame.get_size()
		sw, sh = screen.get_size()
		scale = get_window_scale((fw, fh), (sw, sh))
		scaled_frame = pg.transform.scale(frame, (fw*scale, fh*scale))
		fw, fh = scaled_frame.get_size()

		# blit final frame
		screen.fill((0,0,0))
		screen.blit(scaled_frame, ((sw-fw)/2, (sh-fh)/2))
		pg.display.update()
		clock.tick(60)
	
	pg.quit()

if __name__ == '__main__':
	main()
