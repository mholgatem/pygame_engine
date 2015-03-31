import pygame
from pygame.locals import *

class Controller(object):
	def __init__(self):
		#key press repeat -> delay: 300, repeat rate: 20
		pygame.key.set_repeat(10, 20)
		
		#initiate joystick(s)
		pygame.joystick.init()
		js_count = pygame.joystick.get_count()
		self.js = []
		for i in range(js_count):
			self.js.append(pygame.joystick.Joystick(i))
			self.js[i].init()
			
		self.control_mapping = {
				'PAUSE': [K_ESCAPE],
				
				'P1_LEFT': [K_LEFT, {'joystick': 0, 'axis': 0, 'value': -1}],
				'P1_RIGHT': [K_RIGHT, {'joystick': 0, 'axis': 0, 'value': 1}],
				'P1_UP':[K_UP, {'joystick': 0, 'axis': 1, 'value': 1}],
				'P1_DOWN':[K_DOWN, {'joystick': 0, 'axis': 1, 'value': -1}],
				'P1_JUMP':[K_RSHIFT, {'joystick': 0, 'button': 0}],
				'P1_SHOOT':[K_RETURN,  {'joystick': 0, 'button': 1}] ,
				
				'P2_LEFT': [K_a, {'joystick': 1, 'axis': 0, 'value': -1}],
				'P2_RIGHT': [K_d, {'joystick': 1, 'axis': 0, 'value': -1}],
				'P2_UP': [K_w, {'joystick': 1, 'axis': 1, 'value': 1}],
				'P2_DOWN': [K_s, {'joystick': 1, 'axis': 1, 'value': -1}],
				'P2_JUMP': [K_CAPSLOCK,  {'joystick': 1, 'button': 0}],
				'P2_SHOOT': [K_TAB,  {'joystick': 1, 'button': 1}]
				}
		
	def get_action(self):
		
		#if (event.type == pygame.KEYDOWN or
		#		event.type == pygame.KEYUP):
		#			control_check = event.key
		#if event.type == pygame.JOYAXISMOTION:
		#		control_check = {'joystick': event.joy, 'axis': event.axis, 'value': event.value}
		#if (event.type == pygame.JOYBUTTONDOWN or 
		#	event.type == pygame.JOYBUTTONUP):
		#		control_check = {'joystick': event.joy, 'button': event.button}
		
		action_list = []
		for index, key in enumerate(pygame.key.get_pressed()):
			if key: 
				for action, mapped_control in self.control_mapping.iteritems():
					if index in mapped_control:
						action_list.append(action)
						
		if action_list: return action_list
		#for action, mapped_control in self.control_mapping.iteritems():
		#	if control_check in mapped_control: return action
		
		return []
			
					