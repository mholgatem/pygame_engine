import pygame
import game
import animations

#This is where you define all of your sprite objects
#You can use game.animator to create pre-defined animators
class Generic(pygame.sprite.Sprite):
	def __init__(self, image, layer = 4, groups = ()):
		self.groups = groups
		self._layer = layer
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()

	def update(self, corner_index = None):
		pass
		
class Icon(pygame.sprite.Sprite):
	def __init__(self, layer = 4, groups = ()):
		self.groups = groups
		self._layer = layer
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		self.image = pygame.Surface((1, 1), pygame.SRCALPHA, 32).convert()
		self.rect = self.image.get_rect()

	def update(self, corner_index = None):
		pass
	
class Sprite_Sheet(pygame.sprite.Sprite):
	def __init__(self, image, layer = 4, groups = ()):
		self.groups = groups
		self._layer = layer
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		self.path = image
		self.image = pygame.image.load(image)
		self.scaled_image = self.image.copy()
		self.rect = self.image.get_rect()

	def update(self, corner_index = None):
		pass
	
class Button(pygame.sprite.Sprite):

	def __init__(self, text, id, margin = 5, padding = 10, font_size = 12, font_color = None, background_color = None, start_pos=(0,0), enabled = True, layer = 4, groups = None):
		
		self.groups = groups
		self._layer = layer
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		self.font_color = (255,255,255) if not font_color else font_color
		self.background_color = (125,125,125) if not background_color else background_color
		self.margin = margin
		self.padding = padding
		self.font_size = font_size
		self.enabled = enabled
		self.id = id
		
		try:
			text.unlock() #check if already a surface image
		except AttributeError:
			font = pygame.font.Font('assets/font.ttf', self.font_size)
			self.text = text
			text = font.render(self.text, 1, self.font_color, self.background_color)
		
		self.rect = text.get_rect().inflate(self.margin * 2, self.margin * 2)
		self.padding_rect = self.rect.inflate(self.padding * 2, self.padding * 2)
		
		self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA, 32).convert()
		self.image.fill(self.background_color, pygame.Rect(0, 0, self.rect.w, self.rect.h))
		self.image.blit(text,(self.margin, self.margin))
		if not self.enabled: 
			self.image.set_alpha(125)
		
		if start_pos[0] < 0:

			self.padding_rect.topright = (pygame.display.Info().current_w + start_pos[0], start_pos[1])
		else:
			self.padding_rect.topleft = (pygame.display.Info().current_w - 150 + start_pos[0], start_pos[1])
			
		self.rect.center = self.padding_rect.center
	
		
			
	def update(self, action = None):
		pass

class Frame(pygame.sprite.Sprite):

	def __init__(self, rect, layer = 4, index = None, groups = None):
		
		self.groups = groups
		self._layer = layer
		pygame.sprite.Sprite.__init__(self, self.groups)
		
		GREEN = (0,255,0)
		BLACK = (0,0,0)
		WHITE = (255,255,255)
		
		self.rect = rect
		self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.rect(self.image, GREEN, pygame.Rect(0, 0, self.rect.w, self.rect.h), 1)
		self.count = 1
		self.index = index
		
		corner_x = (0, self.rect.w)
		corner_y = (0, self.rect.h)
		self.corners = []
		for x in corner_x:
			for y in corner_y:
				pygame.draw.circle(self.image, GREEN, (x,y), 8)
				pygame.draw.circle(self.image, WHITE, (x,y), 7)
				self.corners.append(pygame.Rect(self.rect.x - 8 + x, self.rect.y - 8 + y, 16, 16))
	
	
	def move_and_update(self, x, y):

		GREEN = (0,255,0)
		BLACK = (0,0,0)
		WHITE = (255,255,255)
		
		self.rect.move_ip(x,y)
		self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.rect(self.image, GREEN, pygame.Rect(0, 0, self.rect.w, self.rect.h), 1)
		
		corner_x = (0, self.rect.w)
		corner_y = (0, self.rect.h)
		self.corners = []
		for x in corner_x:
			for y in corner_y:
				pygame.draw.circle(self.image, GREEN, (x,y), 8)
				pygame.draw.circle(self.image, WHITE, (x,y), 7)
				self.corners.append(pygame.Rect(self.rect.x - 8 + x, self.rect.y - 8 + y, 16, 16))
			
	def update(self, corner_index = None):
		if corner_index != None:
		 #0 - 2
		 #|    |
		 #1 - 3

			if corner_index == 0 or corner_index == 2:
				self.corners[corner_index + 1].x = self.corners[corner_index].x
			if corner_index == 1 or corner_index == 3:
				self.corners[corner_index - 1].x = self.corners[corner_index].x
				
			if corner_index == 0 or corner_index == 1:
				self.corners[corner_index + 2].y = self.corners[corner_index].y
			if corner_index == 2 or corner_index == 3:
				self.corners[corner_index - 2].y = self.corners[corner_index].y
			
			GREEN = (0,255,0)
			CYAN = (0,255,255)
			BLACK = (0,0,0)
			WHITE = (255,255,255)
		
			self.rect = pygame.Rect(self.corners[0].center, (self.corners[2].centerx - self.corners[0].centerx, self.corners[1].centery - self.corners[0].centery))
			self.rect.normalize()
			
			self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA, 32).convert_alpha()
			pygame.draw.rect(self.image, GREEN, pygame.Rect(0, 0, self.rect.w, self.rect.h), 1)
			
			corner_x = (0, self.rect.w)
			corner_y = (0, self.rect.h)

			for x in corner_x:
				for y in corner_y:
					pygame.draw.circle(self.image, GREEN, (x,y), 8)
					pygame.draw.circle(self.image, WHITE, (x,y), 7)
				
		
		
		
		