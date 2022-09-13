import pygame
from pygame.locals import *
from pygame import mixer

# Initializing modules
pygame.init()
mixer.init()

# Screen variables
screen_width = 600
screen_height = 600

from easygui import *

msg = "                           Welcome to Brick N Ball\n\n\n How to Play Brick N Ball \n\n\n Click Anywhere to Start \n\n\n Broke All the bricks by ball \n\n Don't Avoid Ball \n\n Left Movement=LEFT\n Right Movement=RIGHT"
choices = ["Click here to start the game"]
buttonbox(msg, choices=choices)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Brick N Ball")


# Define font
font = pygame.font.SysFont('Constantia', 30)
font2 = pygame.font.SysFont('Algerian', 30)
# define colors
bg = (0, 0, 0)
# block_colors
block_green = (0, 100, 0)
block_white = (255, 255, 255)
block_orange = (255, 165, 0)
# paddle color
paddle_col = (192, 192, 192)
paddle_outline = (200, 100, 100)
# Text color
text_col = (20, 20, 240)
score_col = (20, 200, 20)

# defining game variables
column = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
score = 0


# Fuction for displaying text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# brick wall class
class wall():
    def __init__(self):
        self.width = screen_width // column
        self.height = 50

    def create_wall(self):
        self.blocks = []
        # Defining an empty list for a individual block
        block_individual = []
        for row in range(rows):
            # Reset the block row list
            block_row = []
            # iterate through each coloumn
            for col in range(column):
                # generate x and y position for each block and create rectangle
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # create a list at this point to store the rect and color
                block_individual = [rect, strength]
                # appending individual block to block row
                block_row.append(block_individual)
            # Appending the row in overall block list
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # Assigning color according to strength
                if block[1] == 3:
                    block_col = block_orange
                elif block[1] == 2:
                    block_col = block_white
                elif block[1] == 1:
                    block_col = block_green
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)


class paddle():
    def __init__(self):
        self.reset()

    def move(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        # Defining Paddle variables
        self.height = 20
        self.width = int(screen_width / column)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 6
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0


# Class ball
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self, score):

        # Collison Threshold - Distance when we will consider that collison has occured
        Collison_thresh = 5

        # Start off with the assumption that wall has destroyed completely
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # Check Collison
                if self.rect.colliderect(item[0]):
                    #bounce_fx.play()
                    self.score += 10
                    # Check if collison is from above
                    if abs(self.rect.bottom - item[0].top) < Collison_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # Check if collison is from below
                    if abs(self.rect.top - item[0].bottom) < Collison_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # Check if collison is from left
                    if abs(self.rect.right - item[0].left) < Collison_thresh and self.speed_x > 0:
                        self.speed_y *= -1
                    # Check if collison is from right
                    if abs(self.rect.left - item[0].right) < Collison_thresh and self.speed_x < 0:
                        self.speed_y *= -1
                        # Reduce the block strength
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                # Check if block still exists, in which case wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                # Increase item counter
                item_count += 1

                # Increase row count
            row_count += 1

        # After Iterating through all the walls, check if wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

        # Check for collison with blocks
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # Check for collison with top and bottom
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # Checking collison with paddle
        if self.rect.colliderect(player_paddle):

            # Check if colliding from top
            if abs(self.rect.bottom - player_paddle.rect.top) < Collison_thresh and self.speed_y > 0:
                self.speed_y *= -1
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over
        # return self.score

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 1)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0
        self.score = 0


# Create wall
wall = wall()
wall.create_wall()

# Create paddle
player_paddle = paddle()

# Create ball
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:

    clock.tick(fps)
    screen.fill(bg)
    # draw all objects
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        # draw paddle
        player_paddle.move()
        # draw ball
        game_over = ball.move(score)
        if game_over != 0:
            live_ball = False

    # Print player instructions
    if not live_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST', font, text_col, 240, screen_height // 2 + 50)
            draw_text('CLICK ANYWHERE TO START', font, text_col, 100, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
    score = ball.score
    draw_text(f"{score}", font2, score_col, 50, screen_height - 50)
    pygame.display.update()
pygame.quit()