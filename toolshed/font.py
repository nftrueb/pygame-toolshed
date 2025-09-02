from dataclasses import dataclass

import pygame as pg 

@dataclass
class Dialogue: 
	text: str 
	bounding_box: pg.Rect 
	word_wrap: bool = True 
	debug: bool = False

class FontSpriteWriter: 
	def __init__(self, sprite_sheet, sprite_w=8, sprite_h=8): 
		self.sprite_sheet = sprite_sheet
		self.sprite_w = sprite_w 
		self.sprite_h = sprite_h 

		self.font = {}
		for i in range(10): 
			self.font[str(i)] = (i*sprite_w, 8)

		for i in range(26): 
			self.font[chr(i+65)] = (sprite_w * i, 0)

		self.font[' '] = (80, 8)
		self.font['.'] = (88, 8)

	def __repr__(self): 
		s = '' 
		for key, value in self.font.items(): 
			s += f'{key}: {value} |'
		return s 
	
	def get_size(self, text): 
		return (len(text) * self.sprite_w, self.sprite_h)


	def render(self, surf: pg.Surface, dialogue: Dialogue): 
		rect = dialogue.bounding_box
		pos = (rect[0], rect[1])
		dim = (rect[2], rect[3])

		# create a variable length surface to contain the entire string
		string_surf = pg.Surface(dim)
		string_surf.set_colorkey((255,0,255))
		string_surf.fill((255, 0, 255))

		# controls cursor so text can wrap 
		x_offset, y_offset = 0, 0

		for idx, character in enumerate(dialogue.text): 
			# if not character.isdigit(): 
			# 	print(f'ERROR: could not render character: {character}')
			# 	continue 

			if 'a' <= character <= 'z': 
				character = chr(ord(character)-32)

			if character == '\n': 
				x_offset = 0
				y_offset += 1
				continue

			# self.font maps character to the offset in the sprite sheet
			area = (self.font[character][0], self.font[character][1], self.sprite_w, self.sprite_h)
			string_surf.blit(self.sprite_sheet, dest=(x_offset*self.sprite_w, y_offset*self.sprite_h), area=area)

			x_offset += 1
			if dialogue.word_wrap: 
				if x_offset * self.sprite_w > dim[0] - self.sprite_w: 
					if y_offset * self.sprite_h > dim[1] - self.sprite_h: 
						break 
					x_offset = 0 
					y_offset += 1

		# draw outline of bounding box
		if dialogue.debug: 
			pg.draw.rect(surf,(255,0,0), (pos[0], pos[1], dim[0]-1, dim[1]-1), width=1)

		# draw text 
		surf.blit(string_surf, dest=pos)
