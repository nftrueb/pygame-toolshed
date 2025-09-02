from dataclasses import dataclass, field
from typing import List
from copy import copy 

import pygame as pg

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
	ROOT_TAG = 'root'

	def __init__(self, debug=False): 
		self.root = Node(tag=self.ROOT_TAG, bounds=None)
		self.debug = debug

	def __repr__(self): 
		s = f'UI(\n{self.root}\n)'
		return s 
	
	def draw(self, surf): 
		if self.debug:
			rect = pg.Rect(
				self.root.bounds.x-1, 
				self.root.bounds.y-1, 
				self.root.bounds.w+2, 
				self.root.bounds.h+2
			)
			pg.draw.rect(surf, (255,0,0), rect, width=1)

		for node in self.root.children: 
			width = 1 
			if isinstance(node, Node) and node.filled: 
				width = 0
			pg.draw.rect(surf, (100,100,100), node.bounds, width)

	def insert(self, new_node: Node, parent_tag: str = ''): 
		if self.root.bounds is None: 
			self.root.children.append(new_node) 
			self.root.bounds = copy(new_node.bounds)
			return 
		
		# search for the correct parent node to insert into if parent tag was specified
		if parent_tag != '':
			for node in self.root.children: 
				if node.tag == parent_tag: 
					node.children.append(new_node)
					self.extend_bounds(node, new_node)
					return 
		
		# no node was found so insert at current level
		self.root.children.append(new_node)
		self.extend_bounds(self.root, new_node)
		
	def insert_recursive(self, node: Node, input: Node): 
		pass 

	def remove(self): 
		pass 

	def get_node(self, pos): 
		return self.get_node_rec(self.root, pos)
	
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
