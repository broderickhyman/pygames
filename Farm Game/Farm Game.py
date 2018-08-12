import pygame
import sys
import time
import random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
time_start = time.time()

WindowHeight = 800
WindowWidth = 800
H = WindowHeight
W = WindowWidth
Screen = pygame.display.set_mode((WindowWidth, WindowHeight), 0, 32)
pygame.display.set_caption('Farm Game')

Black = (0, 0, 0)
Green = (0, 150, 0)
White = (255, 255, 255)
Blue = (0, 0, 200)
Red = (200, 0, 0)
Purple = (128, 0, 128)
Pink = (255, 105, 180)

width_scale = int(W / 4)
height_scale = int(H / 4)

field1 = {'rect':pygame.Rect(W * 3 / 32,   H * 5 / 32,  width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field2 = {'rect':pygame.Rect(W * 3 / 8,    H * 5 / 32,  width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field3 = {'rect':pygame.Rect(W * 21 / 32,  H * 5 / 32,  width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field4 = {'rect':pygame.Rect(W * 3 / 32,   H * 7 / 16,  width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field5 = {'rect':pygame.Rect(W * 3 / 8,    H * 7 / 16,  width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field6 = {'rect':pygame.Rect(W * 21 / 32,  H * 7 / 16,  width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field7 = {'rect':pygame.Rect(W * 3 / 32,   H * 23 / 32, width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field8 = {'rect':pygame.Rect(W * 3 / 8,    H * 23 / 32, width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
field9 = {'rect':pygame.Rect(W * 21 / 32,  H * 23 / 32, width_scale, height_scale), 'grow':False, 'time1':0, 'growth':0, 'crop':0, 'color':Blue, 'seeds':0,'speed':1}
fields = [field1, field2, field3, field4, field5, field6, field7, field8, field9]

image_crop_1 = pygame.image.load('plant1.jpg')
image_crop_2 = pygame.image.load('plant2.jpg')
image_crop_3 = pygame.image.load('plant3.jpg')
image_crop_4 = pygame.image.load('plant4.jpg')
image_crop_5 = pygame.image.load('plant5.jpg')
image_crop_1 = pygame.transform.scale(image_crop_1, (width_scale,height_scale))
image_crop_2 = pygame.transform.scale(image_crop_2, (width_scale,height_scale))
image_crop_3 = pygame.transform.scale(image_crop_3, (width_scale,height_scale))
image_crop_4 = pygame.transform.scale(image_crop_4, (width_scale,height_scale))
image_crop_5 = pygame.transform.scale(image_crop_5, (width_scale,height_scale))

plant_button = pygame.Rect(W * 3 / 32,          H / 32, W / 8, H / 16)
harvest_button = pygame.Rect(W * 3 / 32 + W / 16 + W / 8, H / 32, W / 8, H / 16)

type_1 = 1
type_2 = 2
type_3 = 3

plant_1 = {'rect':pygame.Rect(W / 16,       H / 2 - H / 8, width_scale, height_scale),   'crop':type_1}
plant_2 = {'rect':pygame.Rect(W / 8 + width_scale,    H / 2 - H / 8, width_scale, height_scale),   'crop':type_2}
plant_3 = {'rect':pygame.Rect(W * 3 / 16 + W / 2, H / 2 - H / 8, width_scale, height_scale),   'crop':type_3}
plants = [plant_1,plant_2,plant_3]

exit_button = pygame.Rect(0,0,W / 16, H / 16)

def text(text,color1,color2,top,left,font1=30):
    Font = pygame.font.SysFont(None, font1)
    text = Font.render(text,True,color1,color2)
    text_rect = text.get_rect()
    text_rect.top = top
    text_rect.left = left
    return text,text_rect

bushels = 0
Click = False
Harvest = False
harvest_x = -10
harvest_y = -10
Planting = False
crop_type = 0
plant_x = -10
plant_y = -10
Plant_select = False
speed = 1
seeds = 9

HS_file = open('FarmGameHS.txt','r')
for line in HS_file:
    HS_old = line
HS_file.close()



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == MOUSEBUTTONUP:
            if Harvest == False:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                Click = True
            if Harvest == True:
                harvest_x = event.pos[0]
                harvest_y = event.pos[1]
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                Click = True

    while Click == True:
        for i in fields:
            if i['rect'].collidepoint(mouse_x,mouse_y):
                if Planting == True:
                    if seeds > 0:
                        if i['grow'] == False:
                            i['speed'] = random.randint(1,5)
                            i['grow'] = True
                            i['crop'] = crop_type
                            i['time1'] = time.time()
                            Click = False
                            Plant_select = False
                            #print 'Grow'
                            seeds -= 1
            else:
                Click = False
        
        if harvest_button.collidepoint(mouse_x,mouse_y):
            if Harvest == True:
                Harvest = False
                print('Stop Harvest')
                Click = False
            else:
                Planting = False
                Harvest = True
                Click = False
                print('Harvest')
            mouse_x = -10
            mouse_y = -10
            

        if plant_button.collidepoint(mouse_x,mouse_y):
            if Planting == True:
                Planting = False
                print('Stop Plant')
            else:
                #Plant_select = True
                Click = False
                Harvest = False
                Planting = True
                mouse_x = -10
                mouse_y = -10
                crop_type = type_1
                print('Plant')

        if exit_button.collidepoint(mouse_x,mouse_y):
            if int(HS_old) < bushels:
                HS_new = str(bushels)
                open('FarmGameHS.txt','w').close()
                HS_file = open('FarmGameHS.txt','w')
                HS_file.write(HS_new)
                HS_file.close()
            pygame.quit()
            sys.exit(0)

    while Plant_select == True:
        Screen.fill(Black)
        Screen.blit(image_crop_5, plant_1['rect'])
        pygame.draw.rect(Screen, Pink, plant_2['rect'])
        pygame.draw.rect(Screen, Red, plant_3['rect'])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == MOUSEBUTTONUP:
                plant_x = event.pos[0]
                plant_y = event.pos[1]

        for i in plants:
            if i['rect'].collidepoint(plant_x,plant_y):
                crop_type = i['crop']
                plant_x = -10
                plant_y = -10
                Plant_select = False
                Planting = True

        
        pygame.display.flip()
        clock.tick(10)
            
    Screen.fill(Black)

    for i in fields:
        pygame.draw.rect(Screen, i['color'], i['rect'])
        
    pygame.draw.rect(Screen, Green, plant_button)
    pygame.draw.rect(Screen, Green, harvest_button)
    pygame.draw.rect(Screen, Red, exit_button)
    
    for i in fields:
        if i['grow'] == True:
            if i['crop'] == type_1:
                time2 = time.time()
                dif = time2 - i['time1']
                speed = i['speed']
                if dif < speed:
                     Screen.blit(image_crop_1, i['rect'])
                if (dif > speed) and (dif < 2 * speed):
                    Screen.blit(image_crop_2, i['rect'])
                    i['growth'] = 10
                if (dif > 2 * speed) and (dif < 3 * speed):
                    Screen.blit(image_crop_3, i['rect'])
                    i['growth'] = 20
                if (dif > 3 * speed) and (dif < 4 * speed):
                    Screen.blit(image_crop_4, i['rect'])
                    i['growth'] = 50
                    #i['seeds'] = 1
                if (dif > 4 * speed) and (dif < 6000):
                    Screen.blit(image_crop_5, i['rect'])
                    i['growth'] = 100
                    random1 = 1#random.randint(1,2)
                    if random1 == 1:
                        random2 = random.randint(0,3)
                    #if random1 == 2:
                    #    random2 = random.randint(0,1)
                    i['seeds'] = random2 * speed / 4
            if i['crop'] == type_2:
                i['color'] = Pink
            if i['crop'] == type_3:
                i['color'] = Red
                    
        if Harvest == True:
            for i in fields:
                if i['rect'].collidepoint(harvest_x,harvest_y):
                    i['grow'] = False
                    i['color'] = Blue
                    bushels = bushels + i['growth']
                    seeds += i['seeds']
                    i['growth'] = 0
                    i['seeds'] = 0
                    harvest_x = -10
                    harvest_y = -10
                    #print 'Stop Grow'

        if seeds < 5:
            random1 = random.randint(0,3)
        else:
            random1 = random.randint(0,2)

    time_now = time.time()
    time_dif = int(time_now - time_start)
    time_dif_min = str(int(time_dif / 60))
    time_dif_sec = str(time_dif % 60)
    if len(time_dif_sec) == 1:
        time_dif_sec = '0' + time_dif_sec
    time_elapsed = 'Time Played = ' + time_dif_min + ':' + time_dif_sec
                

    text1 = 'Bushels Harvested: ' + str(bushels)
    text2 = 'Seeds: ' + str(seeds)
    text3 = 'High Score: ' + HS_old
    
    P1,P2 = text(text1, Red, Black, H / 32, W / 2)
    Screen.blit(P1,P2)
    P5,P6 = text('Plant', Black, Green, plant_button.top + (plant_button.bottom - plant_button.top) / 4, plant_button.left + (plant_button.right - plant_button.left) / 4)
    Screen.blit(P5,P6)
    P7,P8 = text('Harvest', Black, Green, harvest_button.top + (harvest_button.bottom - harvest_button.top) / 4, harvest_button.left + (harvest_button.right - harvest_button.left) / 8)
    Screen.blit(P7,P8)
    P9,P10 = text(text2, Red, Black, P2.bottom, P2.left)
    Screen.blit(P9,P10)
    P13,P14 = text('X', Black, Red, 0, W / 80, 70)
    Screen.blit(P13,P14)
    P15,P16 = text(text3, Red, Black, P10.bottom, P10.left)
    Screen.blit(P15,P16)
    P21,P22 = text(time_elapsed, Red, Black,0 , P10.left)
    Screen.blit(P21,P22)

    pygame.display.flip()
    clock.tick(20)
