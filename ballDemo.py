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

pygame.init()

clock = pygame.time.Clock()

width = 800 
height = 600
size = width, height


bgColor = r,g,b = 0, 0, 10

screen = pygame.display.set_mode(size)

bgImage = pygame.image.load("images/Screens/Start Screen.png").convert()
bgRect = bgImage.get_rect()

balls = pygame.sprite.Group()
players = pygame.sprite.Group()
hudItems = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
blocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all = pygame.sprite.OrderedUpdates()

Ball.containers = (all, balls)
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
					player.go("up")
				if event.key == pygame.K_d:
					player.go("right")
				if event.key == pygame.K_s:
					player.go("down")
				if event.key == pygame.K_a:
					player.go("left")
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					b = player.attack("dorito")
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					player.go("stop up")
				if event.key == pygame.K_d:
					player.go("stop right")
				if event.key == pygame.K_s:
					player.go("stop down")
				if event.key == pygame.K_a:
					player.go("stop left")
				elif (event.key == pygame.MOUSEBUTTONUP):
					b = player.shoot("stop")		
								
		if len(balls) < 10:
			if random.randint(0, 1*60) == 0:
				Ball("images/Ball/Snoop Dogg.png",
						  [random.randint(0,10), random.randint(0,10)],
						  [random.randint(100, width-100), random.randint(100, height-100)])
						  
						  
		if timerWait < timerWaitMax:
			timerWait += 1
		else:
			timerWait = 0
			timer.increaseScore(.1)
		
		playersHitBalls = pygame.sprite.groupcollide(players, balls, False, True)
		ballsHitBalls = pygame.sprite.groupcollide(balls, balls, False, False)
		bulletsHitBalls = pygame.sprite.groupcollide(bullets, balls, True , True)
		playersHitBlocks = pygame.sprite.groupcollide(players, blocks, False, False)
		
		for player in playersHitBlocks:
			for block in playersHitBlocks[player]:
				player.collideBlock(block)
		
		for player in playersHitBalls:
			for ball in playersHitBalls[player]:
				score.increaseScore(1)
				
		for bullet in playersHitBalls:
			for ball in playersHitBalls[player]:
				score.increaseScore(1)
				
		for bully in ballsHitBalls:
			for victem in ballsHitBalls[bully]:
				bully.collideBall(victem)
		
		all.update(width, height, blocks)
		
		dirty = all.draw(screen)
		pygame.display.update(dirty)
		pygame.display.flip()
		clock.tick(60)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
