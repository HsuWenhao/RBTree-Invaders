import pygame 
from laser import Laser

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,constraint,speed):
		super().__init__()
		self.image = pygame.image.load('../graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.max_x_constraint = constraint
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 1200

		self.lasers = pygame.sprite.Group()

		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.laser_sound.set_volume(0.5)

	def get_input(self,control_array):
		if control_array != []:
			move = control_array.pop(0)
			if move == 1:
				self.rect.x += self.speed
			elif move == -1:
				self.rect.x -= self.speed

		if self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()

	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.right = self.max_x_constraint
			
		if self.rect.right >= self.max_x_constraint:
			self.rect.left = 0

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.midtop,-20,self.rect.bottom))

	def update(self,control_array):
		self.get_input(control_array)
		self.constraint()
		self.recharge()
		self.lasers.update()
