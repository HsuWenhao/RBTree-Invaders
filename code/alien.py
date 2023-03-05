import pygame

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = '../graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))

		if color == 'red': self.value = 1
		elif color == 'green': self.value = 2
		else: self.value = 3

	def update(self,direction,halt = False):
		if not halt:
			self.rect.x += direction*50

class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		self.image = pygame.image.load('../graphics/extra.png').convert_alpha()
		
		if side == 'right':
			x = screen_width + 50
			self.speed = - 3
		else:
			x = -50
			self.speed = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed