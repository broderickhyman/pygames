import pygame
import sys
import time
import math
import random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
all_fonts = pygame.font.get_fonts()
basicFont = pygame.font.SysFont('arial', 20)

W = 800
H = 500

Surface = pygame.display.set_mode((W,H), 0, 32)
pygame.display.set_caption('Jetpack')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
color_list = [GREEN, WHITE, BLUE, RED, YELLOW]

def text_print(text,color1,color2,left,top,Font=basicFont):
    text = Font.render(text,True,color1,color2)
    text_rect = text.get_rect()
    text_rect.top = top
    text_rect.left = left
    Surface.blit(text, text_rect)

class Coin(object):
    def __init__(self, x, y, width=10, height=10, color=YELLOW):
        self.step = 0
        self.start_x = x
        self.start_y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.start_x - width / 2,self.start_y - height / 2,width,height)
        self.remove = False
    def update(self):
        self.step += 1
        self.rect.left = self.start_x - (self.step * 5)
        if self.rect.right < -1:
            self.remove = True
        return self.remove
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

HEIGHT1 = 30

ceiling = pygame.Rect(0,0,W,HEIGHT1)
ground = pygame.Rect(0,H - HEIGHT1,W,HEIGHT1)
player = pygame.Rect(50,H / 2,40,80)

game = True
pause = False
lifting = False
falling = True
change_y = 0
time_dif = 0
time1 = time.time()
time2 = time.time()
distance = 0
coins_collected = 0
coins = []
coin_removal = []
VERTICAL_SPEED = 8
#coins.append(Coin(W,H/2))
while game == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            if event.key == K_p:
                if pause:
                    pause = False
                else:
                    pause = True
        if event.type == KEYDOWN:
            if event.key == pygame.K_w:
                if event.mod & pygame.KMOD_LMETA:
                    pygame.quit()
                    sys.exit(0)
        if event.type == MOUSEBUTTONDOWN:
            falling = False
            lifting = True
        if event.type == MOUSEBUTTONUP:
            lifting = False
            falling = True

    for item in coins:
        test = item.update()
        if item.rect.colliderect(player):
            coins_collected += 1
            test = True
        if test:
            coin_removal.append(item)

    

    for item in coin_removal:
        coins.remove(item)
    coin_removal = []
        
    distance += .1

    if distance > 10:
        rand1 = random.randint(50,H - 50)
        rand2 = random.randint(1,10)
        rand3 = random.randint(1,5)
        for i in range(0,rand2):
            for j in range(0,rand3):
                coins.append(Coin(W + i * 20,rand1 + j * 20))
        distance = 0

    time2 = time.time()
    time_dif = time2 - time1
    if falling:
        change_y = change_y + 15 * time_dif
        time1 = time.time()
    else:
        if lifting:
            change_y = change_y + -15 * time_dif
            time1 = time.time()

    if change_y > VERTICAL_SPEED:
        change_y = VERTICAL_SPEED
    else:
        if change_y < -VERTICAL_SPEED:
            change_y = -VERTICAL_SPEED

    player.top += change_y

    if player.bottom > H - HEIGHT1:
         player.bottom = H - HEIGHT1
         change_y = 0
    else:
        if player.top < HEIGHT1:
            player.top = HEIGHT1
            change_y = 0

    Surface.fill(BLACK)

    for item in coins:
        item.draw(Surface)



    pygame.draw.rect(Surface, GREEN, ground)
    pygame.draw.rect(Surface, BLUE, ceiling)
    pygame.draw.rect(Surface, RED, player)
    

    text_print('Coins Collected: ' + str(coins_collected), GREEN, BLACK, 500, 30)
    
    pygame.display.flip()
    mainClock.tick(100)
