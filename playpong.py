import pygame
import button
from easygui import *
#from tkinter import *
#create display window
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 480
WHITE = (255, 255, 255)+
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('P-PONG(Python Programs Collection of Native Games)')


#load button images
Name_img = pygame.image.load('Name.png').convert_alpha()
brick_img = pygame.image.load('brick.png').convert_alpha()
tict_img = pygame.image.load('tict.png').convert_alpha()
pong_img = pygame.image.load('pong.png').convert_alpha()
snake_img = pygame.image.load('snake.png').convert_alpha()
turt_img = pygame.image.load('turt.png').convert_alpha()

#create button instances
Name_button = button.Button(40, 20, Name_img, 0.8)
brick_button = button.Button(80, 160, brick_img, 0.8)
tict_button = button.Button(80, 260, tict_img, 0.8)
pong_button = button.Button(80, 360, pong_img, 0.8)
snake_button = button.Button(80, 460, snake_img, 0.8)
turt_button = button.Button(80, 560, turt_img, 0.8)

#game loop
run = True
while run:

	screen.fill(WHITE)

	if Name_button.draw(screen):
		print('START')
	if brick_button.draw(screen):
		print('START')
		import brick
	if tict_button.draw(screen):
		print('START')
		import tictactoe
	if pong_button.draw(screen):
		print('START')
		import pong0
	if snake_button.draw(screen):
		print('START')
		import snake0
	if turt_button.draw(screen):
		print('START')
		import Turtle


	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()