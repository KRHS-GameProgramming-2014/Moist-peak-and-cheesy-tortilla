import pygame, sys, math

class Player(pygame.sprite.Sprite):
	def __init__(self, pos = [300,400], size = [100,100]):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.images = [pygame.image.load("images/Mr. MLG.PNG"),
							pygame.image.load("images/RightFootForward.PNG"),
							pygame.image.load("images/Mr. MLG.PNG"),
							pygame.image.load("images/LeftFootForward.PNG")]
		self.changed = False
		self.stopImage = pygame.image.load("images/Mr. MLG.PNG")
		self.frame = 0
		self.maxFrame = len(self.images) - 1
		self.waitCount = 0
		self.maxWait = 60*.25
		self.baseImage = self.images[self.frame]
		self.image = self.images[self.frame]
		self.rect = self.image.get_rect(center = pos)
		self.maxSpeed = 10
		self.speedx = 0
		self.speedy = 0
		self.shooting = False
		self.moving = False
		self.pistolCount = 0
		self.maxPistolCount = 100000000
		self.pistolCoolDown = 0
		self.pistolCoolDownMax = 50
		self.pistoldelay = 5
		self.damage = 40
	
	def update(*args):
		self = args[0]
		width = args[1]
		height = args[2]
		self.move()
		self.animate()
		self.changed = False
		
	#~ def attack(self, atk):
		#~ if atk == "pistol" and self.pistolCoolDown == 0:
			#~ self.shooting = True
			#~ self.pistolCoolDown = self.pistolCoolDownMax
			#~ return [Pistol(self)]
		#~ '''if atk == "spray" and self.sprayCoolDown == 0:
			#~ self.spraying = True
			#~ self.sprayCoolDown = self.sprayCoolDownMax
			#~ return [Spray(self)]'''
		#~ return []
		
		
	def move(self):
		self.speed = [self.speedx, self.speedy]
		self.rect = self.rect.move(self.speed)
		self.moving = True
		
	def animate(self):
		if self.waitCount < self.maxWait:
			self.waitCount += 1
		else:
			self.waitCount = 0
			self.changed = True
			if self.frame < self.maxFrame:
				self.frame += 1
			else:
				self.frame = 0
		
		
		if self.moving:
			self.baseImage = self.images[self.frame]    
		if not self.moving:
			self.baseImage = self.stopImage
		mousePos = pygame.mouse.get_pos()
		mousePosPlayerX = mousePos[0] - self.rect.center[0]
		mousePosPlayerY = mousePos[1] - self.rect.center[1]
		self.angle = ((math.atan2(mousePosPlayerY, mousePosPlayerX))/math.pi)*180
		self.angle = -self.angle
		rot_image = pygame.transform.rotate(self.baseImage, self.angle)
		rot_rect = self.rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect)
		self.image = rot_image
		self.moving = False
	
	def go(self, direction):
		if direction == "up":
			self.speedy = -self.maxSpeed
		elif direction == "stop up":
			self.speedy = 0
		elif direction == "down":
			self.speedy = self.maxSpeed
		elif direction == "stop down":
			self.speedy = 0
			
		if direction == "right":
			self.speedx = self.maxSpeed
		elif direction == "stop right":
			self.speedx = 0
		elif direction == "left":
			self.speedx = -self.maxSpeed
		elif direction == "stop left":
			self.speedx = 0

	#def shoot(self, option=None):
		#if option == None:
			#return Bullet(self.rect.center, self.angle)
