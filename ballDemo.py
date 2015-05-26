import pygame, sys, random, math
from Ball import Ball
from Player import Player
from HUD import Text
from HUD import Score
from Button import Button
from BackGround import BackGround
from Level import Level
from Block import Block
from Bullet import Bullet
from Enemy import Enemy

pygame.init()

clock = pygame.time.Clock()

width = 800 
height = 600
size = width, height


bgColor = r,g,b = 0, 0, 10

screen = pygame.display.set_mode(size)

bgImage = pygame.image.load("images/Screens/Start Screen.png").convert()
bgRect = bgImage.get_rect()

enemies = pygame.sprite.Group()
players = pygame.sprite.Group()
hudItems = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
blocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all = pygame.sprite.OrderedUpdates()

Enemy.containers = (all, enemies)
Player.containers = (all, players)
BackGround.containers = (all, backgrounds)
Bullet.containers = (all, bullets)
Block.containers = (all, blocks)
Score.containers = (all, hudItems)



run = False

startButton = Button([width/2, height-300], 
					 "images/Buttons/Start Base.png", 
					 "images/Buttons/Start Clicked.png")

while True:
	while not run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					run = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				startButton.click(event.pos)
			if event.type == pygame.MOUSEBUTTONUP:
				if startButton.release(event.pos):
					run = True
					
		bgColor = r,g,b
		screen.fill(bgColor)
		screen.blit(bgImage, bgRect)
		screen.blit(startButton.image, startButton.rect)
		pygame.display.flip()
		clock.tick(60)
		
	BackGround("images/Floors/Brick Floor.png")
	
	player = Player([width/2, height/2])
	
	
	level = Level(size, 40)
	level.loadLevel("1")

	timer = Score([80, height - 25], "Time: ", 36)
	timerWait = 0
	timerWaitMax = 6

	score = Score([width-80, height-25], "Score: ", 36)
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					player.speedy += -8
				if event.key == pygame.K_d:
					player.speedx += 8
				if event.key == pygame.K_s:
					player.speedy += 8
				if event.key == pygame.K_a:
					player.speedx += -8
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					b = player.attack("dorito")
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					player.speedy -= -8
				if event.key == pygame.K_d:
					player.speedx -= 8
				if event.key == pygame.K_s:
					player.speedy -= 8
				if event.key == pygame.K_a:
					player.speedx -= -8
				elif (event.key == pygame.MOUSEBUTTONUP):
					b = player.shoot("stop")		
								
		if len(enemies) < 10:
			if random.randint(0, 2*60) == 0:
				Enemy([400,400],
					  [80,80],
					  [5,0])
						  
						  
		if timerWait < timerWaitMax:
			timerWait += 1
		else:
			timerWait = 0
			timer.increaseScore(.1)
		
		playersHitEnemies = pygame.sprite.groupcollide(players, enemies, False, True)
		enemiesHitEnemies = pygame.sprite.groupcollide(enemies, enemies, False, False)
		bulletsHitEnemies = pygame.sprite.groupcollide(bullets, enemies, True , True)
		playersHitBlocks = pygame.sprite.groupcollide(players, blocks, False, False)
		
		for player in playersHitBlocks:
			for block in playersHitBlocks[player]:
				player.collideBlock(block)
		
		for player in playersHitEnemies:
			for enemy in playersHitEnemies[player]:
				score.increaseScore(1)
				
		for bullet in bulletsHitEnemies:
			for enemy in bulletsHitEnemies[bullet]:
				score.increaseScore(1)
				
		for bully in enemiesHitEnemies:
			for victem in enemiesHitEnemies[bully]:
				bully.collideEnemy(victem)
		
		all.update(width, height, blocks)
		
		dirty = all.draw(screen)
		pygame.display.update(dirty)
		pygame.display.flip()
		clock.tick(60)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
