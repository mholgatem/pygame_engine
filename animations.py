import pygame
import game

#this is where you can define your animations
class Player(object):
	def __init__(self, sprite_sheet):
	
		self.start = game.Animator(title = "start", 
													sprite_sheet = sprite_sheet, 
													number_of_frames = 8,
													animation_area = pygame.Rect(0,0,243,52), 
													frame_list = [
													(0,0,15,52),
													(15,0,25,52),
													(40,0,35,52),
													(75,0,35,52),
													(110,0,33,52),
													(143,0,32,52),
													(175,0,35,52),
													(210,0,33,52)],
													speed=10, 
													loop = False)
													
		self.run = game.Animator(title = "run", 
													sprite_sheet = sprite_sheet, 
													number_of_frames = 11,
													animation_area = pygame.Rect(0,0,633,52), 
													frame_list = [
													(319,0,30,52),
													(349,0,21,52),(371,0,23,52),
													(394,0,32,52),(426,0,33,52),
													(459,0,28,52),(487,0,24,52),
													(511,0,26,52),(537,0,32,52),
													(570,0,34,52),(604,0,30,52)], 
													loop = True, 
													loop_start_frame = 1, 
													no_wait = False)
													
		self.idle = game.Animator(title = "idle", 
													sprite_sheet = sprite_sheet, 
													number_of_frames = 5,
													animation_area = pygame.Rect(246,0,64,52), 
													frame_list = [
													(0,0,30,52),
													(0,0,30,52),
													(0,0,30,52),
													(34,0,30,52),
													(0,0,30,52)],
													speed = 200,
													loop = True, test = (200,200))
													
class Sonic(object):
	def __init__(self, sprite_sheet):
		
		self.idle = game.Animator(title = "idle", 
													sprite_sheet = sprite_sheet, 
													number_of_frames = 4,
													animation_area = pygame.Rect(270,0,180,45),
													speed = 200,
													loop = True)
													
		self.run = game.Animator(title = "run", 
												sprite_sheet = sprite_sheet, 
												number_of_frames = 12,
												animation_area = pygame.Rect(0,45,540,45), 
												loop = True,
												loop_start_frame = 9)
												
		