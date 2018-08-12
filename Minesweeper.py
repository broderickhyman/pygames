import pygame
import sys
import time
import random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
all_fonts = pygame.font.get_fonts()
basicFont = pygame.font.SysFont('arial', 20)

W = 550
H = 550

Surface = pygame.display.set_mode((W,H), 0, 32)
pygame.display.set_caption('Template')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)



def text_print(text,color1,color2,left,top,Font=basicFont):
    text = Font.render(text,True,color1,color2)
    text_rect = text.get_rect()
    text_rect.top = top
    text_rect.left = left
    Surface.blit(text, text_rect)

class Tile(object):
    def __init__(self,left,top,column,row,sur=0,width=40,height=40,color=WHITE):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(left,top,width,height)
        self.mine = False
        self.flag = False
        self.click = False
        self.column = column
        self.row = row
        self.sur = sur

def new_mines():
    for item in tile_list:
        item.mine = False
        item.color = WHITE
        item.click = False
        item.flag = False
    for i in range(0,mines):
        add = True
        while (add == True):
            row = random.randint(0,9)
            col = random.randint(1,9)
            num = (row * 10 + col)
            if (tile_list[num].mine == False):
                tile_list[num].mine = True
                #tile_list[num].color=RED
                add = False
    for item in tile_list:
        row = item.row
        col = item.column
        sur = 0
        for tile in tile_list:
            if tile.row <= row + 1 and tile.row >= row - 1:
                if tile.column <= col + 1 and tile.column >= col - 1:
                    if tile.mine == True:
                        sur += 1
        item.sur = sur
        

game = True
tile_list = []
mines = 15
click = False
button = 99
POS = (0,0)
state = -1

reset = pygame.Rect(W - 100,0,100,50)

for i in range(0,10):
    for j in range(0,10):
        tile_list.append(Tile(65 + i * 42,100 + j * 42,i + 1,j + 1))
        
new_mines()
        

while game == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        if event.type == MOUSEBUTTONUP:
            click = True
            button = event.button
            pos = event.pos
        if event.type == MOUSEMOTION:
            POS = event.pos
            
    if click:
        if reset.collidepoint(pos):
            state = -1
            mines = 15
            new_mines()
        if state == -1:
            for item in tile_list:
                if item.rect.collidepoint(pos):
                    if button == 1:
                        if item.mine == False:
                            item.click = True
                            if item.sur == 0:
                                for var in tile_list:
                                    if var.sur == 0:
                                        var.click = True
                        else:
                            item.color = RED
                            #mines -=1
                            state = 1
                            #game = False
                    if button == 3:
                        if item.flag == False:
                            item.flag = True
                            item.color = GREEN
                            mines -= 1
                        else:
                            if item.flag == True:
                                item.flag = False
                                item.color = WHITE
                                mines += 1
        click = False
        button = 99
        


    if mines == 0:
        unflagged = 0
        for item in tile_list:
            if item.mine == True and item.flag == False:
                unflagged += 1
        if unflagged == 0:
            state = 0

    Surface.fill(BLACK)

    pygame.draw.rect(Surface, RED, reset)

    for item in tile_list:
        pygame.draw.rect(Surface, item.color, item.rect)
        if item.mine == False and item.click == True:
            if item.sur == 0:
                col1 = BLACK
            if item.sur == 1:
                col1 = BLUE
            if item.sur == 2:
                col1 = GREEN
            if item.sur == 3:
                col1 = RED
            if item.sur == 4:
                col1 = YELLOW
            if item.sur > 4:
                col1 = BLACK
            text_print(str(item.sur),col1,WHITE,item.rect.centerx - 8,item.rect.centery - 10)
            #text_print(str(item.row)+','+str(item.column),BLACK,WHITE,item.rect.left,item.rect.top)


    text_print('Mines:' + str(mines),RED,BLACK,W / 2 - 45,10)
    text_print('RESET',BLACK,RED,reset.left + 17,reset.top + 13)

    if state == 0:
        text_print('YOU WON!',RED,WHITE,W / 2 - 55,50)
    else:
        if state == 1:
            text_print('You Lost... :(',RED,WHITE,W / 2 - 55,50)

    #text_print(str(POS[0])+','+str(POS[1]),RED,BLACK,10,10)

    pygame.display.flip()
    mainClock.tick(100)
