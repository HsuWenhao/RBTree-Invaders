import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
import RBTree
from button import Button
class Game:
	def __init__(self):
		# Block A setting
		self.tick_count = 0
		self.move_down = 0
		self.halt = False
		self.new_command = []
		self.control_sequence = []
		# Block A setup

		# Player setup
		player_sprite = Player((block_width-20-100,block_height),block_width,50)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# health and score setup
		self.lives = 3
		self.live_surf = pygame.image.load('../graphics/heart.png').convert_alpha()
		self.live_x_start_pos = block_width - 140
		self.score = 0
		self.font = pygame.font.Font('../font/Pixeled.ttf',16)
		self.font_2 = pygame.font.Font('../font/Minecraft.ttf',16)
		# Obstacle setup
		self.shape = obstacle.shape
		self.block_size = 4
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 6
		self.obstacle_x_positions = [num * 50 for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = 0, y_start = 480) # x_start = block_width / 15

		# Control Panel setup
		self.buttons = []
		self.create_buttons(300,450,10)


		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 3, cols = 3) # Alien sprite group spawn
		self.alien_direction = 1 # inatial moving direction
		
		
		# Audio
		music = pygame.mixer.Sound('../audio/music.wav')
		music.set_volume(0.2)
		music.play(loops = -1)
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.explosion_sound.set_volume(0.3)

	def create_obstacle(self, x_start, y_start,offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_buttons(self,x_start, y_start,offset_x): # create control panel
		button_size = 48
		i = 0
		for row in range(2):
			for col in range(10):
				x = x_start + col * button_size + offset_x
				y= y_start + row * button_size
				button = Button(text = str(i),width=32,height=32,pos = (x,y),elevation=5,val = i,font = self.font_2)
				self.buttons.append(button)
				i += 1


	def create_multiple_obstacles(self,*offset,x_start,y_start):
		for offset_x in offset:
			self.create_obstacle(x_start,y_start,offset_x)

	def alien_setup(self,rows,cols,x_distance = 50,y_distance = 48,x_offset = 0, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index == 0: alien_sprite = Alien('yellow',x,y)
				elif row_index ==1: alien_sprite = Alien('green',x,y)
				else: alien_sprite = Alien('red',x,y)
				self.aliens.add(alien_sprite)

	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		if self.move_down:
			for alien in all_aliens:
					self.alien_move_down(1)
					self.halt = False
			self.move_down = 0
		else:
			for alien in all_aliens:
				if alien.rect.right >= block_width:
					self.alien_direction = -1
					self.halt = True
					self.move_down = 1
				elif alien.rect.left <= 0:
					self.alien_direction = 1
					self.halt = True
					self.move_down = 1

	def alien_move_down(self,distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.midbottom,20,block_height)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def collision_checks(self):
		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()

				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					laser.kill()
					self.explosion_sound.play()

		# alien lasers & lasers lasers
		if self.alien_lasers:
			for laser in self.alien_lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					if self.lives <= 0:
						pygame.quit()
						sys.exit()

		# aliens obstacle
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien,self.blocks,True)
				if pygame.sprite.spritecollide(alien,self.player,False):
					pygame.quit()
					sys.exit()

	def display_lives(self):
		x = self.live_x_start_pos
		screen.blit(self.live_surf,(x,8))
		live_surf = self.font.render(f'x {self.lives}',False,'white')
		screen.blit(live_surf,(x+36,-4))

	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-4))
		screen.blit(score_surf,score_rect)

	def display_things(self):
		line_1 = self.font.render('|',False,'green')
		line_2 = self.font.render('---',False,'green')
		frame = pygame.image.load('../graphics/FRAME.png')
		screen.blit(frame,(block_width,0))
		for i in range(15): # 300*600
			screen.blit(line_1,(block_width,i*50))
			screen.blit(line_2,(block_width+10+i*50,400))
		
		control_surf = self.font_2.render(f'CONTROL SEQ: {str(self.control_sequence).replace("-1","<").replace("1",">")}',False,'white')
		screen.blit(control_surf,(320,560))

	def display_tree(self):
		rbtree = pygame.image.load('../graphics/Source.gv.png')
		rbtree = pygame.transform.smoothscale(rbtree,(420,346))
		screen.blit(rbtree,(331,35))

	def victory_message(self):
		if not self.aliens.sprites():
			victory_surf = self.font.render('You won',False,'white')
			victory_rect = victory_surf.get_rect(center = (block_width / 2, block_height / 2))
			screen.blit(victory_surf,victory_rect)

	def run(self):
		self.tick_count += 1
		pushed_seq = []
		for button in self.buttons:
			button.draw(screen)
			temp = button.update()
			if temp:
				pushed_seq.append(temp)
		for [c,v] in pushed_seq:
			if c == 1:
				self.new_command = my_tree.insert(v)
			elif c == -1:
				self.new_command = my_tree.delete(my_tree.search(v))
			my_tree.draw()
		pushed_seq = []
		if self.tick_count >= 30:  # 1 tick per 30 frame, just like some old school arcade games
			self.alien_lasers.update()
			self.aliens.update(self.alien_direction,self.halt)
			self.alien_position_checker()
			self.player.update(self.control_sequence)
			self.tick_count = 0
			if self.new_command:
				self.control_sequence += self.new_command
				self.new_command = []
			# print(self.control_sequence)
			
			self.collision_checks()

			

		
		self.player.sprite.lasers.draw(screen)
		self.player.draw(screen)
		self.blocks.draw(screen)
		self.aliens.draw(screen)
		self.alien_lasers.draw(screen)
		self.display_tree()
		self.display_lives()
		self.display_score()
		self.victory_message()
		crt.draw(crt_scan)
		self.display_things()

		


class CRT:
	def __init__(self):
		self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()
		# self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))
	def create_crt_lines(self,count):
		line_height = 3
		line_amount = int(425 / line_height)
		for line in range(line_amount):
			y_pos = line * line_height 
			pygame.draw.line(self.tv,'white',(0,y_pos),(screen_width,y_pos),1)
		y_pos = count * line_height
		pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)
	def draw(self,count):
		self.count = count
		self.tv.set_alpha(randint(80,90))
		self.create_crt_lines(self.count)
		screen.blit(self.tv,(331,35))

if __name__ == '__main__':
	pygame.init()
	screen_width = 800
	screen_height = 600


	block_width = 290 # Block A
	block_height = 600

	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game()
	
	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,6000)
	crt_scan = -40
	crt = CRT()
	my_tree =RBTree.RedBlackTree() 


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == ALIENLASER:
				game.alien_shoot()

		screen.fill((30,30,30))
		game.run()
		crt_scan += 1
		if crt_scan >= 300:

			crt_scan = 0
		pygame.display.flip()
		clock.tick(60)
