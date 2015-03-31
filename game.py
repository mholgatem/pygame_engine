import pygame
import os
from controller import Controller


class Game(object):
	
	GRAVITY_FORCE = 9.81 #meters per second
	
	def __init__(self, screen_size = (0,0), fullscreen = True):
		#clear command line for incoming error messages
		os.system('clear')
		self.screen = self.init_screen(screen_size, fullscreen)
		self.screen_width = pygame.display.Info().current_w
		self.screen_height = pygame.display.Info().current_h
		self.controller = Controller()
		self.blank_layer = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.SRCALPHA, 32).convert_alpha()
		
		self.frames_per_second = 20
		self.pixels_per_meter = 20

	def init_screen(self, size, fullscreen):

		pygame.init()
		pygame.display.init()
		dinfo = pygame.display.Info()

		flag = 0
		if fullscreen:
			flag = pygame.FULLSCREEN
		#return pygame.display.set_mode(size, flag, 32)

		if (pygame.display.mode_ok((dinfo.current_w, dinfo.current_h),pygame.FULLSCREEN)):
			return pygame.display.set_mode(size, flag)
		else:
			pygame.quit()
			sys.exit()
	
	def set_background(self, background_image):
		self.background_image = pygame.image.load(background_image)
		self.background_rect = self.background_image.get_rect()

		scale = min(float(self.background_rect.w) / float(self.screen_width), float(self.background_rect.h) / float(self.screen_height))
		self.background_rect = (int(self.background_rect.w / scale), int(self.background_rect.h / scale))
		
		self.clean_background = pygame.transform.smoothscale(self.background_image, self.background_rect) #USE THIS TO RESET BACKGROUND
		self.background = self.clean_background.copy() #MAKE CHANGES AND USE THIS ONE TO BLIT TO SCREEN
		self.background_rect = self.background_image.get_rect()
		self.screen.blit(self.background_image, (0,0))
		pygame.display.flip()
	
	def get_input(self, event_type = [pygame.KEYDOWN, pygame.KEYUP, pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION], return_events = False ):
		events = pygame.event.get(event_type)
		if return_events:
			return (self.controller.get_action(), events)
		return self.controller.get_action()
	
	def set_number_of_layers(self, number_of_layers):
		self.layers = [self.blank_layer.copy() for x in number_of_layers]
		return self.layers
		
	def update_sprite(self, sprite, **kwargs):
		#remove sprite (old location/previous animation frame)
		self.screen.blit(self.background_image, sprite.rect, sprite.rect)
		#update sprite
		sprite.update(**kwargs)
		#blit sprite
		#self.screen.blit(sprite.image, sprite.rect)
	
	def gravity(self):
		return (self.GRAVITY_FORCE * self.pixels_per_meter) / self.frames_per_second #add this to y velocity every frame
	
	class tooltip(object):
		def __init__(self, text, fg_color = (255,255,255), bg_color = (83,83,83), font_size = 12):
			self.font = pygame.font.Font('assets/font.ttf', font_size) #for labeling frames
			self.image = self.font.render(text, 1, fg_color, bg_color)
			self.rect = self.image.get_rect()
		
		
class velocity(object):
	def __init__(self):
		self.x = 0
		self.y = 0
	def set_x(self, amt):
		self.x = amt
	def set_y(self, amt):
		self.y = amt
	def add_x(self, amt, limit = None):
		self.x += amt
		if limit: #max velocity (+ or -)
			limit = abs(limit)
			self.x = min(limit, max(self.x, -limit))
	def add_y(self, amt, limit = None):
		self.y += amt
		if limit: #max velocity (+ or -)
			limit = abs(limit)
			self.y = min(limit, max(self.y, -limit))
	def bleed_x(self, amt = 1):
		#bleed to 0
		self.x = int(((self.x + .1) /abs(self.x + .1)) * max((abs(self.x) - amt), 0))
	def bleed_y(self, amt = 1):
		#bleed to 0
		self.y = int(((self.y + .1) /abs(self.y + .1)) * max((abs(self.y) - amt), 0))
	def update(self, rect):
		rect.x += self.x
		rect.y += self.y
		return rect
		
class Animator(object):
	
	#direction = 0 -> vertical, direction = 1 -> horizontal
	def __init__(self, title, sprite_sheet, number_of_frames = 1, animation_area = None, frame_list = None, start_frame = 0, direction = 1, loop = True, loop_start_frame = 0, speed = None, pause = 0, test = False):
		
		self.title = title #Any title can be given, just helps in identification
		#print self.title, frame_list, number_of_frames
		#build animation sprite sheet
		self.sprite_sheet = pygame.Surface((animation_area.w, animation_area.h), pygame.SRCALPHA, 32).convert_alpha()
		self.sprite_sheet.blit(sprite_sheet, (0,0), animation_area)
		
		#number_of_frames can be used to evenly divide the sprite sheet (if all frames are same size)
		#If frames vary in size, pass a list of rects with frame_list
		self.frame_count = number_of_frames #if not frame_list else len(frame_list)
		self.animation_area = animation_area if animation_area else self.sprite_sheet.get_rect()
		self.pause = pause #number of game frames to pause animation
		self.finished_run = False #finished running, only validate when loop = False
		self.anim_speed = speed #number of milliseconds between each frame
		self.last_update = pygame.time.get_ticks()
		
		#divide animation_area / frame_count to create frame_list
		
		if not frame_list:
			frame_list = []
			if direction == 0: #VERTICAL SPRITE SHEET
				frame_size = pygame.Rect(0,0, self.animation_area.w, self.animation_area.h / self.frame_count)
				for _ in xrange(self.frame_count):
					frame_list.append(frame_size.copy())
					frame_size.y += frame_size.h
			if direction == 1: #HORIZONTAL SPRITE SHEET
				frame_size = pygame.Rect(0,0, self.animation_area.w / self.frame_count, self.animation_area.h)
				for _ in xrange(number_of_frames):
					frame_list.append(frame_size.copy())
					frame_size.x += frame_size.w
					
		
		self.frame_list = [pygame.Rect(x) for x in frame_list] #Make sure everything is pygame.Rect
					
					
		self.current_frame = min(self.frame_count - 1, start_frame)
		self.direction = direction
		self.loop = loop
		self.loop_start_frame = loop_start_frame
		
		self.image = pygame.Surface((self.frame_list[self.current_frame].w, self.frame_list[self.current_frame].h), pygame.SRCALPHA, 32).convert_alpha()
		self.image.blit(self.sprite_sheet, (0,0), self.frame_list[self.current_frame])
		self.rect = self.image.get_rect()
		self.test = self.test_animation(test)
		
		
	def update(self, set_frame = None, frame_rate = 1):

		if self.pause >= 0:
			if self.anim_speed == None or ((pygame.time.get_ticks() - self.last_update) > self.anim_speed):
				next_frame = self.current_frame + frame_rate
				if set_frame is not None: 
					self.current_frame = set_frame
				else:
					if not self.loop:
						self.current_frame = min(max(0,next_frame), self.frame_count - 1)
						if self.current_frame == self.frame_count - 1: self.finished_run = True
					else:
						if next_frame < 0:
							self.current_frame = self.frame_count - 1
						elif next_frame >= self.frame_count:
							self.current_frame = self.loop_start_frame
						else:
							self.current_frame = next_frame
							

				self.image = pygame.Surface((self.frame_list[self.current_frame].w, self.frame_list[self.current_frame].h), pygame.SRCALPHA, 32).convert_alpha()
				self.image.blit(self.sprite_sheet, (0,0), self.frame_list[self.current_frame])
				if self.test:
					self.image.blit(self.font.render(str(self.current_frame),1,(255,0,255)), (0,0))
					self.image = pygame.transform.smoothscale(self.image, (100,100) if self.test == True else self.test)
				self.rect = self.image.get_rect()
				self.last_update = pygame.time.get_ticks()
		else:
			self.pause -= 1
				
	def test_animation(self, test):
		if test:
			self.anim_speed = 1000
			self.font = pygame.font.Font('assets/font.ttf', 12) #for labeling frames
			self.image.blit(self.font.render(str(self.current_frame),1,(255,0,255)), (0,0))
			self.image = pygame.transform.smoothscale(self.image, (100,100) if test == True else test)
		return test
		
	
	
class Groups(object):
	def __init__(self):
		self.layer_objects = pygame.sprite.LayeredUpdates() #ALL OBJECTS EXCEPT BACKGROUND
		self.players = pygame.sprite.Group() #PLAYERS
		self.gravity = pygame.sprite.Group() #GRAVITY WILL AFFECT THIS ITEM
		self.animated = pygame.sprite.Group() #SPRITES THAT HAVE ANIMATION
		self.enemies = pygame.sprite.Group() #ENEMIES
		self.tangible = pygame.sprite.Group() #STOPS PLAYER MOVEMENT (PLATFORMS, WALLS, ENEMIES?)

		
		
		