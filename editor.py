import pygame
import game
import sprites
import glob
import os

class Editor(object):
	def __init__(self):
		self.running = True
		self.timer = pygame.time.Clock()
		self.Game = game.Game()
		self.screen = self.Game.screen
		self.update_rects = []
		
		self.Game.set_background('assets/images/background.jpg')
		self.Game.frames_per_second = 60
		
		self.layer_objects = pygame.sprite.LayeredUpdates() #ALL OBJECTS EXCEPT BACKGROUND
		self.buttons = pygame.sprite.LayeredUpdates() 
		self.popup_buttons = pygame.sprite.LayeredUpdates()
		self.frames = pygame.sprite.LayeredUpdates() 
		self.animated = pygame.sprite.Group() #SPRITES THAT HAVE ANIMATION
		
		self.tool_bar = pygame.Rect(self.Game.screen_width - 150, 0, 150, self.Game.screen_height)
		self.sprite_work_area = pygame.Rect(0,0, self.Game.screen_width - 150, self.Game.screen_height)
		self.spritesheet = None
		self.run = None
		
		#draw tool_bar to clean background, so we can avoid re-drawing every time we clean the background.
		self.Game.clean_background.fill((80,80,80), self.tool_bar)
		self.Game.background = self.Game.clean_background.copy()
		self.screen.blit(self.Game.background, (0,0))
		pygame.display.flip()
		
		self.path_to_assets = os.path.realpath('./assets/images/')
		self.Main()
	
	def rect_from_point(self, pos1, pos2 = None):
		if not pos2: pos2 = pos1
		width = abs(pos1[0] - pos2[0])
		height = abs(pos1[1] - pos2[1])
		start_point = ( min(pos1[0], pos2[0]), min(pos1[1], pos2[1]) )
		
		return pygame.Rect(start_point, (width, height))
	
	def open_file(self, path = None):
		path = path if path else self.path_to_assets
		if os.path.isfile(path):
			self.spritesheet = sprites.Sprite_Sheet(image = path)
			self.Game.background = self.Game.clean_background.copy()
			self.Game.background.blit(self.spritesheet.image, self.sprite_work_area.topleft)
			self.screen.blit(self.Game.background, self.sprite_work_area.topleft)
			
			for button in self.popup_buttons:
				button.kill()
				
			self.layer_objects.clear(self.screen, self.Game.background)
			self.layer_objects.draw(self.screen)
			pygame.draw.rect(self.screen, (255,255,255), self.sprite_work_area, 2)
			pygame.display.flip()
										
		else:	
			files = []
			extensions = ['.gif', '.jpg', '.png']
			files = [sprites.Button(file, ('self.open_file(path = "%s")' % os.path.join(path, file)), groups = (self.popup_buttons, self.layer_objects), start_pos = (-140, 20 * index))
						for index, file in enumerate(os.listdir(path)) if file[-4:].lower() in extensions]
			#self.popup_buttons.add(files)
		
		
	def grab_corner(self, point, frames):
		for frame in frames:
			for index, corner in enumerate(frame.corners):
				if corner.collidepoint(point) and frame.rect.collidepoint(point):
					return {'frame': frame, 'corner': corner, 'index': index}
		return False
	
	def zoom_in(self):
		self.scale += 1
		for frame in self.frames:
			frame.rect.move_ip((frame.rect.x)  , frame.rect.y)
			topleft = frame.rect.topleft
			frame.rect.inflate_ip(frame.rect.w, frame.rect.h )
			frame.rect.topleft = topleft
			frame.update_rect()
		self.Game.background = self.Game.clean_background.copy()
		if self.spritesheet:
			self.spritesheet.rect.inflate_ip(self.spritesheet.rect.w, self.spritesheet.rect.h)
			self.spritesheet.rect.topleft = (0,0)
			try: self.spritesheet.scaled_image = pygame.transform.smoothscale(self.spritesheet.image, (self.spritesheet.rect.w, self.spritesheet.rect.h))
			except: self.spritesheet.scaled_image = pygame.transform.scale(self.spritesheet.image, (self.spritesheet.rect.w, self.spritesheet.rect.h))
			self.Game.background.blit(self.spritesheet.scaled_image, self.sprite_work_area.topleft)
		self.screen.blit(self.Game.background, (0,0))
		pygame.display.flip()
	
	def zoom_out(self):
		self.scale -= 1
		for frame in self.frames:
			frame.rect.move_ip((frame.rect.x * -.5) , (frame.rect.y  * -.5) )
			topleft = frame.rect.topleft
			frame.rect.inflate_ip((frame.rect.w  * -.5) , (frame.rect.h  * -.5) )
			frame.rect.topleft = topleft
			frame.update_rect()
		self.Game.background = self.Game.clean_background.copy()
		if self.spritesheet:
			self.spritesheet.rect.inflate_ip((self.spritesheet.rect.w  * -.5) , (self.spritesheet.rect.h  * -.5) )
			self.spritesheet.rect.topleft = (0,0)
			try: self.spritesheet.scaled_image = pygame.transform.smoothscale(self.spritesheet.image, (self.spritesheet.rect.w, self.spritesheet.rect.h))
			except: self.spritesheet.scaled_image = pygame.transform.scale(self.spritesheet.image, (self.spritesheet.rect.w, self.spritesheet.rect.h))
			self.Game.background.blit(self.spritesheet.scaled_image, self.sprite_work_area.topleft)
		self.screen.blit(self.Game.background, (0,0))
		pygame.display.flip()
	
	def get_item_clicked(self, group, pos):
		for item in group:
			if item.rect.collidepoint(pos):
				return item
		return None
	
	def handle_events(self):
		self.actions = self.Game.get_input()
		self.mouse_events = pygame.event.get([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
		
		for event in self.mouse_events:

			#CLICK BUTTONS
			if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						clicked_buttons = self.buttons.get_sprites_at(pygame.mouse.get_pos())
						clicked_buttons.extend(self.popup_buttons.get_sprites_at(pygame.mouse.get_pos()))
						for button in clicked_buttons:
							if button.enabled:
								exec(button.id)
								break
								
			#WORK AREA ACTIONS		
			if self.sprite_work_area.collidepoint(pygame.mouse.get_pos()):
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					#ZOOM IN
					if event.button == 4 and self.scale < 3:
						self.zoom_in()
					#ZOOM OUT
					if event.button == 5 and self.scale >= 0:
						self.zoom_out()
					#GRAB CORNER/CREATE NEW FRAME
					if pygame.mouse.get_pressed()[0]:
						self.grab_frame = self.grab_corner(pygame.mouse.get_pos(), self.frames)
						if not self.grab_frame:
							self.draw_area = self.rect_from_point(pygame.mouse.get_pos())
							frame = sprites.Frame(rect = self.draw_area.inflate(2,2), groups = (self.frames, self.layer_objects), index = len(self.frames), layer = 5)
							self.grab_frame = self.grab_corner(pygame.mouse.get_pos(), [frame])
					#DELETE FRAME
					if pygame.mouse.get_pressed()[2]:
						clicked_frames = self.frames.get_sprites_at(pygame.mouse.get_pos())
						if clicked_frames:
							clicked_frames[-1].kill()
						for index, frame in enumerate(self.frames):
							frame.index = index
						
								
				
				if event.type == pygame.MOUSEBUTTONUP:
					#KILL FRAME IF TOO SMALL
					if event.button == 1:
						if (self.grab_frame['frame'].rect.w < 10 or
							self.grab_frame['frame'].rect.h < 10) :
								self.grab_frame['frame'].kill()
						self.grab_frame = False
					#UPDATE PREVIEW ANIMATION
					self.rects = [frame.rect.move(-self.sprite_work_area.left,0) for frame in self.frames]
					if self.rects:
						self.run = game.Animator(title = "run", 
												sprite_sheet = self.spritesheet.scaled_image, 
												number_of_frames = len(self.frames),
												animation_area = self.spritesheet.rect,#self.rects[0].unionall(self.rects), 
												frame_list = self.rects, 
												speed = 100,
												loop = True, 
												loop_start_frame = 0)
												#test = True)
				#RESIZE FRAME
				if pygame.mouse.get_pressed()[0] and event.type == pygame.MOUSEMOTION:
					if self.grab_frame:
						self.clear_area = self.grab_frame['frame'].rect.inflate(2,2)
						self.screen.blit(self.Game.background, self.clear_area, self.clear_area)
						mouse_x, mouse_y = pygame.mouse.get_pos()
						x_values = [x for frame in self.frames if frame is not self.grab_frame['frame'] for x in (frame.rect.left, frame.rect.right) if x-10 < mouse_x < x +10]
						y_values = [y for frame in self.frames if frame is not self.grab_frame['frame'] for y in (frame.rect.top, frame.rect.bottom) if y-10 < mouse_y < y +10]
						if x_values:mouse_x = x_values[0]
						if y_values:mouse_y = y_values[0]

								
						self.grab_frame['corner'].center = (mouse_x, mouse_y)
						self.grab_frame['frame'].update(corner_index = self.grab_frame['index'])

						
			else:
				#TOOLBAR
				pass
			
		if 'PAUSE' in self.actions: self.running = False
			
			
	def Main(self):	
		self.button1 = sprites.Button('Load Spritesheet', 'self.open_file()', groups = (self.buttons, self.layer_objects), start_pos = (10, 10))
		self.button2 = sprites.Button(pygame.image.load('assets/images/p1.gif'), 'button2', enabled = False, groups = (self.buttons, self.layer_objects), start_pos = (50,50))
		
		#screen.blit(Game.background_image,(0,0))
		self.layer_objects.draw(self.screen)
		
		self.scale = 1
		
		self.grab_frame = None
		self.draw_area = None
		while self.running:

			self.timer.tick(self.Game.frames_per_second) #max fps
			self.handle_events()
			
			#self.update_rects.extend([item.rect for item in self.layer_objects.sprites()])
			self.layer_objects.clear(self.screen, self.Game.background)
			self.update_rects.extend(self.layer_objects.draw(self.screen))
			
			
			if self.run: 
				self.screen.fill((80,80,80), self.run.rect)
				self.update_rects.append(self.run.rect)
				self.run.update()
				self.run.rect.top = 200
				self.screen.blit(self.run.image, (0,200))
				self.update_rects.append(self.run.rect)
			#self.popup_buttons.clear(self.screen, self.Game.background_image)
			#self.popup_buttons.draw(self.screen)
			
			#self.frames.clear(self.screen, self.Game.background_image)
			#self.frames.draw(self.screen)
			
			pygame.display.update(self.update_rects)
			self.update_rects = []
			pygame.event.pump()


editor = Editor()