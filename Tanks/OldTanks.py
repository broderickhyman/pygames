import pygame, sys, random, math, time
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
basicFont = pygame.font.SysFont(None, 30)

WINDOWWIDTH = 800
WINDOWHEIGHT = 400
W = WINDOWWIDTH
H = WINDOWHEIGHT
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Tanks')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

MOVESPEED = 4
DLEFT = 1
DRIGHT = 3
ULEFT = 7
URIGHT = 9

start_x = WINDOWWIDTH/2-5
start_y = WINDOWHEIGHT-60

ground = pygame.Rect(0,WINDOWHEIGHT - 50,WINDOWWIDTH,50)
player = pygame.Rect(WINDOWWIDTH/2-20, WINDOWHEIGHT-90, 40, 40)
bullet = pygame.Rect(-20, -20, 10, 10)
power_minus = pygame.Rect(555, 25, 20, 20)
power_plus = pygame.Rect(715, 25, 20, 20)
aimer = pygame.Rect(-20, -20, 10, 10)
landpt = pygame.Rect(-20, -20, 10, 10)

def rand_gen():
    random1 = random.randint(0,1)
    if random1 == 0:
        random2 = random.randint(40,W/2 - 80)
    if random1 == 1:
        random2 = random.randint(W/2 + 80, W-40)
    return random2

random_enemy_loc = rand_gen()
enemy = pygame.Rect(random_enemy_loc,H - 90, 40, 40)

def blast():
    centerx = bullet.centerx - 45
    centery = bullet.centery - 60
    images = []
    master_image = pygame.image.load('explosion.png')
    master_image = pygame.transform.scale(master_image, (560, 80))
    master_width, master_height = master_image.get_size()
    for i in range(0,7):
        images.append(master_image.subsurface((i*80,0,80,80)))
    for i in range(0,6):
        windowSurface.blit(images[i],(centerx,centery))
        pygame.display.flip()
        mainClock.tick(10)

def text_print(text,color1,color2,left,top,font1=30):
    Font = pygame.font.SysFont(None, font1)
    text = Font.render(text,True,color1,color2)
    text_rect = text.get_rect()
    text_rect.top = top
    text_rect.left = left
    windowSurface.blit(text, text_rect)
    #return text,text_rect

def enemy_angle_power_update():
    enemy_angle = random.randint(angle_min,angle_max)
    enemy_angle_x = math.cos(math.radians(enemy_angle - 180))
    enemy_angle_y = math.sin(math.radians(enemy_angle))
    enemy_power = random.randint(3,7)
    return enemy_angle_x,enemy_angle_y,enemy_power

def shooting_start():
    start_x = bullet.left
    start_y = bullet.top
    sec = 1
    flying = True
    time1 = time.time()
    return start_x,start_y,sec,flying,time1
   

ymax = 0
flying = False
enemy_flying = False
count = 1
sec = 1
draw = False
damage = 0
enemy_health = 100
player_health = 100
move_left = False
move_right = False
Movespeed = 4
power = 5
new_power = 0
angle = 145
new_angle = 40
angle_up = False
angle_down = False
Cheat = False


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if flying == False and enemy_flying == False:
            if event.type == MOUSEBUTTONUP:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]
                if power_minus.collidepoint(mouse_x,mouse_y):
                    power -=1
                elif power_plus.collidepoint(mouse_x,mouse_y):
                    power +=1
                else:
                    bullet = pygame.Rect(player.centerx-5, player.top + 30, 10, 10)
                    start_x,start_y,sec,flying,time1 = shooting_start()

        if event.type == KEYDOWN and flying == False:
            if event.key == K_LEFT or event.key == ord('a'):
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == ord('d'):
                move_left = False
                move_right = True
            if event.key == K_UP:
                angle_up = True
            if event.key == K_DOWN:
                angle_down = True
                
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == ord('a'):
                move_left = False
            if event.key == K_RIGHT or event.key == ord('d'):
                move_right = False
            if flying == False:
                if event.key == K_EQUALS:
                    power +=1
                if event.key == K_MINUS:
                    power -=1
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP:
                angle_up = False
            if event.key == K_DOWN:
                angle_down = False
            if event.key == K_SPACE:
                if flying == False and enemy_flying == False:
                    bullet = pygame.Rect(player.centerx-5, player.top + 30, 10, 10)
                    start_x,start_y,sec,flying,time1 = shooting_start()

            if event.key == K_RETURN:
                if flying == False and enemy_flying == False:
                    bullet = pygame.Rect(enemy.left + 15, enemy.top + 15, 10, 10)
                    start_x,start_y,sec,enemy_flying,time1 = shooting_start()
                    if enemy.left > player.left:
                        angle_min = 10
                        angle_max = 90
                    else:
                        angle_min = 90
                        angle_max = 170
                    enemy_angle_x,enemy_angle_y,enemy_power = enemy_angle_power_update()
                    
            if event.key == K_e:
                random_enemy_loc = rand_gen()
                enemy_health = 100
                enemy = pygame.Rect(random_enemy_loc,H - 90, 40, 40)
                
            if event.key == K_p:
                player_health = 100
                player = pygame.Rect(W/2-20, H-90, 40, 40)
                aimer_x = angle_x * 50 + player.centerx - 5
                aimer_y = angle_y * -50 + player.bottom - 10
                aimer = pygame.Rect(aimer_x, aimer_y, 10, 10)

            if event.key == K_c:
                if Cheat:
                    Cheat = False
                else:
                    Cheat = True

    if power == 0:
        power = 1
    if power == 11:
        power = 10

    if angle_up is True:
        angle +=1
        mainClock.tick(50)
    if angle_down is True:
        angle -=1
        mainClock.tick(50)
    if angle < 10:
        angle = 10
    if angle > 170:
        angle = 170

    if move_left and player.left > 0:
        player.left -= Movespeed
    if move_right and player.right < WINDOWWIDTH:
        player.right += Movespeed

    if move_left or move_right:
        aimer_x = angle_x * 50 + player.centerx - 5
        aimer_y = angle_y * -50 + player.bottom - 10
        aimer = pygame.Rect(aimer_x, aimer_y, 10, 10)
        landpt = pygame.Rect(player.centerx + int(distance) ,ground.top - 10,10,10)
        new_power = power
    
    if new_angle != angle:     
        angle_x = math.cos(math.radians(angle - 180))
        angle_y = math.sin(math.radians(angle))
        aimer_x = angle_x * 50 + player.centerx - 5
        aimer_y = angle_y * -50 + player.bottom - 10
        aimer = pygame.Rect(aimer_x, aimer_y, 10, 10)
        distance = ((power ** 2) * math.sin(math.radians(angle % 90 *2))) * 10
        if angle_x < 0:
            distance = distance * -1
        landpt = pygame.Rect(player.centerx + int(distance) ,ground.top - 10,10,10)
#        print distance
#        print angle_x,angle_y
        new_angle = angle

    if new_power != power:
        distance = ((power ** 2) * math.sin(math.radians(angle % 90 *2))) * 10
        if angle_x < 0:
            distance = distance * -1
        landpt = pygame.Rect(player.centerx + int(distance) ,ground.top - 10,10,10)
        new_power = power
        
    if flying == True:
        time2 = time.time()
        if (time2-time1) > .001:
            sec += 1
            time1 = time.time()
        move_x = angle_x * power * float(sec)
        move_y = angle_y * power * float(sec) - 5 * (float(sec)/10) ** 2
        bullet.top = start_y - int(move_y)
        bullet.left= start_x + int(move_x)

    if enemy_flying == True:
        time2 = time.time()
        if (time2-time1) > .001:
            sec += 1
            time1 = time.time()
        move_x = enemy_angle_x * 10 * enemy_power * float(sec)/10
        move_y = enemy_angle_y * 10 * enemy_power * float(sec)/10 - 5 * (float(sec)/10) ** 2
        bullet.top = start_y - int(move_y)
        bullet.left= start_x + int(move_x)

    if bullet.left > WINDOWWIDTH or bullet.right < 0:
        flying = False
        enemy_flying = False
        
    if ground.colliderect(bullet):
        blast()
        flying = False
        enemy_flying = False
        impact = pygame.Rect(bullet.centerx - 45,bullet.centery - 62, 80,80)
#        print (bullet.centerx - player.centerx)
        #bullet2 = pygame.Rect(bullet.left, bullet.top, 10, 10)
        if impact.colliderect(enemy):
            dist_x = enemy.centerx - bullet.centerx
            dist_y = enemy.centery - bullet.centery
            dist_mag = abs(float(dist_x))
            damage = (60-dist_mag)/40 * 100
            enemy_health = enemy_health - damage
            damage = 0
        if impact.colliderect(player):
            dist_x = player.centerx - bullet.centerx
            dist_y = player.centery - bullet.centery
            dist_mag = abs(float(dist_x))
            damage = (60-dist_mag)/40 * 100
            player_health = player_health - damage
            damage = 0
            #print 'damage:',damage
            #draw = True
        bullet.top = WINDOWHEIGHT + 20
        bullet.left = WINDOWWIDTH + 20
        
    if enemy.contains(bullet)and flying == True:
        blast()
        flying = False
        bullet.top = WINDOWHEIGHT
        bullet.left = WINDOWWIDTH
        damage = 100
        enemy_health = enemy_health - damage
        damage = 0

    if player.contains(bullet)and enemy_flying == True:
        blast()
        enemy_flying = False
        bullet.top = WINDOWHEIGHT
        bullet.left = WINDOWWIDTH
        damage = 100
        player_health = player_health - damage
        damage = 0

    
    if enemy_health < 0:
        enemy_health = 0
    enemy_health_str = str(enemy_health)
    if player_health < 0:
        player_health = 0
    player_health_str = str(player_health)
    if enemy_health <= 0:
        enemy.top = WINDOWHEIGHT + 50
        enemy.left = WINDOWWIDTH + 50
    if player_health <= 0:
        player.left = W + 200
        aimer.left = W + 200
        landpt.left = W + 200


    windowSurface.fill(BLACK)


    pygame.draw.rect(windowSurface, GREEN, ground)
    pygame.draw.rect(windowSurface, BLUE, player)
    pygame.draw.rect(windowSurface, WHITE, bullet)
    pygame.draw.rect(windowSurface, RED, enemy)
    pygame.draw.rect(windowSurface, GREEN, power_minus)
    pygame.draw.rect(windowSurface, GREEN, power_plus)
    pygame.draw.rect(windowSurface, WHITE, aimer)
    if Cheat:
        pygame.draw.rect(windowSurface, WHITE, landpt)
    

    text = enemy_health_str
    text2 = 'Enemy Health:'
    text3 = 'Player Health:' + player_health_str
    text4 = '-'
    text5 = '+'
    text6 = 'Power:' + str(power)
    text7 = 'Angle:' + str(angle)
    text8 = '(C)heat?'
    text_print(text, WHITE, RED, W-100, 0)
    text_print(text2, WHITE, RED, W-245, 0)
    text_print(text3, WHITE, BLUE, 50, 0)
    text_print(text4, BLACK, GREEN, 560, 25, 28)
    text_print(text5, BLACK, GREEN, 720, 25, 28)
    text_print(text6, BLACK, GREEN, 610, 25, 28)
    text_print(text7, BLACK, GREEN, 600, 50, 28)
    text_print(text8, YELLOW, BLACK, 350, 0, 45)

    pygame.display.flip()
    mainClock.tick(100)
