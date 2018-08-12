import pygame
import sys
import time
import random
import math
import os
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
all_fonts = pygame.font.get_fonts()
basicFont = pygame.font.SysFont(all_fonts[-2], 20)

W = 700
H = 500

Surface = pygame.display.set_mode((W,H), 0, 32)
pygame.display.set_caption('Space Invaders')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

enemies = 30
columns = 8
enemy_list = []

for i in range(0,enemies):
    enemy_list.append(pygame.Rect(60 * (i % columns) + 20,i / columns * 40 + 40,40,20))

block = pygame.Rect(W / 4 - 25, H * 3 / 4, 50, 50)
player = pygame.Rect(W / 2 - 15, H * 9 / 10, 30, 40)
bullet = pygame.Rect(player.centerx - 5, player.centery - 10, 10, 20)

def text_print(text,color1,color2,left,top,font1=30,Font=basicFont):
    #Font = pygame.font.SysFont('Copperplate.ttc', font1)
    text = Font.render(text,True,color1,color2)
    text_rect = text.get_rect()
    text_rect.top = top
    text_rect.left = left
    Surface.blit(text, text_rect)

enemy_right = True
enemy_left = False
player_right = False
player_left = False
shooting = False
shooting_cont = False
time1 = time.time()
time3 = time.time()
total_time = time.time()
MOVEMENT = 10
step_time = .1
fps = 0
fps_avg = 0
fps_count = float(0)
fps_total = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)

            if event.key == K_SPACE:
                shooting_cont = False
            
            if event.key == K_LEFT or event.key == ord('a'):
                player_left = False
            if event.key == K_RIGHT or event.key == ord('d'):
                player_right = False
                
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                player_right = False
                player_left = True
            if event.key == K_RIGHT or event.key == ord('d'):
                player_left = False
                player_right = True

            if event.key == K_SPACE:
                if shooting == False:
                    bullet.centerx = player.centerx
                    bullet.centery = player.centery
                    shooting = True
                    shooting_cont = True
                
#        if event.type == MOUSEBUTTONUP:
#            enemy_list.pop(random.randint(0,len(enemy_list)-1))

    if player_left and player.left > 0:
        player.left -= 4
        if shooting == False:
            bullet.centerx = player.centerx
    if player_right and player.right < W:
        player.right += 4
        if shooting == False:
            bullet.centerx = player.centerx
    
    time2 = time.time()
    dif = time2 - time1
    if dif > step_time:
        for item in enemy_list:
            if enemy_right:
                item.left += MOVEMENT
            if enemy_left:
                item.left -= MOVEMENT
        time1 = time.time()

    time4 = time.time()
    dif2 = time4 - time3
    if dif2 > step_time / 10 and shooting:
        bullet.top -= 20
        if bullet.bottom < 0:
            bullet.center = player.center
            if shooting_cont == False:
                shooting = False
        time3 = time.time()

    for item in enemy_list:
        if item.right > W - 20:
            for item in enemy_list:
                item.top += MOVEMENT * 2
                item.left -= MOVEMENT
            enemy_left = True
            enemy_right = False
            break
        if item.left < 20:
            for item in enemy_list:
                item.top += MOVEMENT * 2
                item.left += MOVEMENT
            enemy_left = False
            enemy_right = True
            break
        if item.colliderect(block):
            enemy_list.remove(item)
        if item.colliderect(bullet):
            enemy_list.remove(item)
            bullet.center = player.center
            if shooting_cont == False:
                shooting = False

    fps +=1
    timestop = time.time()
    if timestop - total_time > .1:
        fps_total += fps
        fps = 0
        fps_count += .1
        fps_avg = float(fps_total) / fps_count
        total_time = time.time()
    

    Surface.fill(BLACK)

    for item in enemy_list:
        pygame.draw.rect(Surface, RED, item)

    pygame.draw.rect(Surface, BLUE, block)
    pygame.draw.rect(Surface, GREEN, player)
    pygame.draw.rect(Surface, WHITE, bullet)

    text_print('FPS - ' + str(round(fps_avg,2)), WHITE, BLACK, 0, 0)

    pygame.display.flip()
    mainClock.tick(100)
