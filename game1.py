import pygame
import game
import sprites

def Main():
	running = True
	timer = pygame.time.Clock()
	Game = game.Game()
	Groups = game.Groups()
	screen = Game.screen
	Game.set_background('assets/images/background.png')
	Game.frames_per_second = 30
	Game.pixels_per_meter = 20 #use to calculate gravity
	
	player1 = sprites.Player(player_number = 1, 
							sprite_sheet = 'megamanx.gif', 
							start_pos = (20,20), 
							groups = (Groups.players, Groups.gravity, Groups.layer_objects, Groups.animated)
							)
							
	#player2 = sprites.Player(player_number = 2, 
							#sprite_sheet = 'megamanx-red.gif', 
							#start_pos = (50,50), 
							#groups = (Groups.players, Groups.gravity, Groups.layer_objects, Groups.animated)
							#)
								
	player2 = sprites.Sonic(player_number = 2, 
							sprite_sheet = 'sonic.gif', 
							start_pos = (600,500), 
							groups = (Groups.players, Groups.gravity, Groups.layer_objects, Groups.animated)
							)
	
	player2.direction = -1
	
	screen.blit(player1.image, player1.rect)
	screen.blit(player2.image, player2.rect)
	pygame.display.flip()

	while running:

		timer.tick(Game.frames_per_second) #max fps
		actions = Game.get_input()
		
		for item in Groups.gravity:
			item.velocity.add_y(Game.gravity())
			
		for item in Groups.animated:
			Game.update_sprite(item)
			
		for action in actions:
			if action == 'PAUSE':
				#exit
				running = False
			else:
				for player in Groups.players:
					Game.update_sprite(player, action=action)
					
		Groups.layer_objects.draw(screen)
		pygame.display.flip()
		pygame.event.pump()

		
Main()