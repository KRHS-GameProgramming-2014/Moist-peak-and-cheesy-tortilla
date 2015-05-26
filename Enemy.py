import pygame, sys, math
from Bullet import Bullet


class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos = [300,400], size = [80,80], speed = [0,0]):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.images = [pygame.image.load("images/enemies/CenterSNOOPDOGG.png"),
							pygame.image.load("images/enemies/LeftSNOOPDOGG.png"),
							pygame.image.load("images/enemies/CenterSNOOPDOGG.png"),
							pygame.image.load("images/enemies/RightSNOOPDOGG.png")
							]
		self.changed = False
		self.speed = speed
		self.stopImage = pygame.image.load("images/enemies/CenterSNOOPDOGG.png")
		self.frame = 0
		self.maxFrame = len(self.images) - 1
		self.waitCount = 0
		self.maxWait = 60*.25
		self.baseImage = self.images[self.frame]
		self.image = self.images[self.frame]
		self.rect = self.image.get_rect(center = pos)
		self.maxSpeed = 10
		self.speedx = speed[0]
		self.speedy = speed[1]
		self.didBounceX = False
		self.didBounceY = False
		self.shooting = False
		self.moving = False
		self.radius = (int(self.rect.height/2.0 + self.rect.width/2.0)/2) - 1
	
	def update(*args):
		self = args[0]
		width = args[1]
		height = args[2]
		blocks = args[3]
		self.move(blocks)
		self.animate()
		self.changed = False
		
		
	def move(self, blocks):
		self.speed = [self.speedx, self.speedy]
		self.moving = True
 
		self.rect = self.rect.move([self.speedx,0])
 
		block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
		for block in block_hit_list:
			if self.speedx > 0:
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right
 
		self.rect = self.rect.move([0,self.speedy])
 
		block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
		for block in block_hit_list:
 
			if self.speedy > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
				
		
		
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
	
	
	def collideBlock(self, other):
		pass
	
	def collideEnemy(self, other):
		if self != other:
			if (self.radius + other.radius) > self.distance(other.rect.center):
				if not self.didBounceX:
					self.speedx = -self.speedx
					self.didBouncex = True
				if not self.didBounceY:
					self.speedy = -self.speedy
					self.didBounceY = True
					
	def distance(self, pt):
		x1 = self.rect.center[0]
		y1 = self.rect.center[1]
		x2 = pt[0]
		y2 = pt[1]
		return math.sqrt(((x2-x1)**2) + ((y2-y1)**2))				
