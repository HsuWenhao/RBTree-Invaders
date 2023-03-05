import pygame, sys
import RBTree

class Button():
	def __init__(self,text,width,height,pos,elevation,val,font):
		#Core attributes 
		super().__init__()
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		self.val = val
		self.font = font
		self.state = 1
		self.pushed = None

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color_green = '#50d070'
		self.top_color_red = '#f14f50'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color_green = '#3d9c54'
		self.bottom_color_red = '#cf3f3f'
		#text
		self.text_surf = self.font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self,screen):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
		if self.state == 1:
			pygame.draw.rect(screen,self.bottom_color_green, self.bottom_rect,border_radius = 12)
			pygame.draw.rect(screen,self.top_color_green, self.top_rect,border_radius = 12)
		else:
			pygame.draw.rect(screen,self.bottom_color_red, self.bottom_rect,border_radius = 12)
			pygame.draw.rect(screen,self.top_color_red, self.top_rect,border_radius = 12)
		screen.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					# do sth
					self.pushed = [self.state,self.val]
					self.state = -self.state
					self.pressed = False
	
	def update(self):
		if self.pushed:
			temp = self.pushed
			self.pushed = None
			return temp
