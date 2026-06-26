from typing import Tuple, List
from copy import copy
from dataclasses import dataclass, field
import pygame as pg
 
WIDTH, HEIGHT = 320,180

@dataclass
class Node: 
	tag: str  = ''
	bounds: pg.Rect = None
	children: List['Node'] = field(default_factory=list)
	filled: bool = False

	def __repr__(self): 
		s = f'Node(tag={self.tag}  bounds={self.bounds}  children=[\n'
		if len(self.children) == 0: 
			s = s[:-1]
		for node in self.children: 
			s += '  ' + str(node) + '\n'
		s += '])'
		return s

class UI: 
	TOP_LEVEL_NODE_TAG = 'top-layer'

	def __init__(self): 
		self.top_level_node = Node(tag=self.TOP_LEVEL_NODE_TAG, bounds=None, )

	def __repr__(self): 
		s = f'UI(\n{str(self.top_level_node)}\n)'
		return s 
	
	def draw(self, surf): 
		rect = pg.Rect(
			self.top_level_node.bounds.x-1, 
			self.top_level_node.bounds.y-1, 
			self.top_level_node.bounds.w+2, 
			self.top_level_node.bounds.h+2
		)
		pg.draw.rect(surf, (255,0,0), rect, width=1)

		for node in self.top_level_node.children: 
			width = 1 
			if isinstance(node, Node) and node.filled: 
				width = 0
			pg.draw.rect(surf, (100,100,100), node.bounds, width)

	def insert(self, new_node: Node, parent_tag: str = ''): 
		if self.top_level_node.bounds is None: 
			self.top_level_node.children.append(new_node) 
			self.top_level_node.bounds = copy(new_node.bounds)
			return 
		
		# search for the correct parent node to insert into if parent tag was specified
		if parent_tag != '':
			for node in self.top_level_node.children: 
				if node.tag == parent_tag: 
					node.children.append(new_node)
					self.extend_bounds(node, new_node)
					return 
		
		# no node was found so insert at current level
		self.top_level_node.children.append(new_node)
		self.extend_bounds(self.top_level_node, new_node)
		
	def insert_recursive(self, node: Node, input: Node): 
		pass 

	def remove(self): 
		pass 

	def get_node(self, pos): 
		return self.get_node_rec(self.top_level_node, pos)
	
	def get_node_rec(self, parent_node, pos): 
		if not parent_node.bounds.collidepoint(pos): 
			return None
		
		# position was found to be in bounding box
		# ... loop through all nodes to find 
		for node in parent_node.children: 
			if node.bounds.collidepoint(pos): 
				return node 
			
		return None
	
	def extend_bounds(self, node, new_node): 
		if new_node.bounds.x + new_node.bounds.w > node.bounds.x + node.bounds.w: 
			node.bounds.w = new_node.bounds.x + new_node.bounds.w - node.bounds.x

		if new_node.bounds.x < node.bounds.x: 
			node.bounds.w = node.bounds.x - new_node.bounds.x + node.bounds.w
			node.bounds.x = new_node.bounds.x

		if new_node.bounds.y + new_node.bounds.h > node.bounds.y + node.bounds.h: 
			node.bounds.h = new_node.bounds.y + new_node.bounds.h - node.bounds.y

		if new_node.bounds.y < node.bounds.y: 
			node.bounds.h = node.bounds.y - new_node.bounds.y + node.bounds.h
			node.bounds.y = new_node.bounds.y


def get_window_scale(src, dest):
	return min(dest[0] // src[0], dest[1] // src[1])

def main():
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

	ui = UI()
	ui_toggle_Node = Node('toggle', pg.Rect(5, 5, 40, 40))
	ui.insert(ui_toggle_Node)

	new_rect = None
	running = True
	edit_ui_mode = True
	while running:
		mx, my = pg.mouse.get_pos()
		mx //= scale 
		my //= scale 

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False

			elif event.type == pg.KEYUP: 
				if event.key == pg.K_SPACE: 
					print(ui)

			elif event.type == pg.MOUSEBUTTONDOWN: 

				node = ui.get_node((mx, my))
				if node and isinstance(node, Node): 
					node.filled = not node.filled
					if node.tag == 'toggle':
						edit_ui_mode = not edit_ui_mode

				else: 
					if edit_ui_mode:
						new_rect = (mx, my)

			elif event.type == pg.MOUSEBUTTONUP: 
				if new_rect is None: 
					continue 

				x = min(new_rect[0], mx)
				y = min(new_rect[1], my)
				w = abs(mx - new_rect[0])
				h = abs(my - new_rect[1])
				node = Node(bounds=pg.Rect(x,y,w,h))
				ui.insert(node)
				new_rect = None 
		
		# clear new frame
		frame.fill((255,255,255))
		
		ui.draw(frame)

		if new_rect: 
			x = min(new_rect[0], mx)
			y = min(new_rect[1], my)
			w = abs(mx - new_rect[0])
			h = abs(my - new_rect[1])
			pg.draw.rect(frame, (100,100,100), (x,y,w,h), width=1)

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
