import pygame, sys, time, math, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
all_fonts = pygame.font.get_fonts()
basicFont = pygame.font.SysFont('arial', 20)

W = 800
H = 600

Surface = pygame.display.set_mode((W,H), 0, 32)
pygame.display.set_caption('Tower Defense')

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
color_list = [GREEN, WHITE, BLUE, RED, YELLOW]

def start():
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    return 'main'

        
        Surface.fill(BLACK)

        Font = pygame.font.SysFont('arial', 45)
        
        text = Font.render('Brodie\'s Tower Defense! :)',True,WHITE)
        text_rect = text.get_rect()
        text_rect.center = (W/2,H/8)
        Surface.blit(text,text_rect)
        text = Font.render('Press Enter to Start a New Game',True,WHITE)
        text_rect = text.get_rect()
        text_rect.center = (W/2,H/2)
        Surface.blit(text,text_rect)

        pygame.display.flip()
        mainClock.tick(100)
    

def main():
    def text_print(text,color1,color2,left,top,Font=basicFont):
        text = Font.render(text,True,color1,color2)
        text_rect = text.get_rect()
        text_rect.top = top
        text_rect.left = left
        Surface.blit(text, text_rect)

    class Tower(object):
        def __init__(self, pos, step=1, width = 40, height=40):
            global color_list
            self.position = pos
            self.width = width
            self.height = height
            self.color = color_list[0]
            self.rect = pygame.Rect(0,0,width,height)
            self.rect.center = pos
            self.time = time.time()
            self.step = step
        def check(self):
            difference = time.time() - self.time
            if difference > self.step:
                self.time = time.time()
                return True
            else:
                return False
        def shoot(self):
            if len(enemies) >= 1:
                target = enemies[0]#random.randint(0,len(enemies)-1)]
                chance = 0#random.randint(0,3)
                if chance == 0:
                    if target.direction == 'down':
                        x_var = target.rect.centerx
                        y_var = target.rect.centery# + 40
                    if target.direction == 'right':
                        x_var = target.rect.centerx# + 40
                        y_var = target.rect.centery
                    if target.direction == 'up':
                        x_var = target.rect.centerx
                        y_var = target.rect.centery# - 40
                if chance >= 1:
                    x_var = random.randint(-50,50) + target.rect.centerx
                    y_var = random.randint(-50,50) + target.rect.centery
##            else:
##                x_var = random.randint(0,W)
##                y_var = random.randint(0,H)
                bullets.append(Bullet(self.rect.center,(x_var,y_var)))
        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)

    class Bullet(object):
        def __init__(self, pos, end_pos, width=20, height=20, color=WHITE):
            self.step = 0
            self.start_x = pos[0]
            self.start_y = pos[1]
            self.end_x = end_pos[0]
            self.end_y = end_pos[1]
            self.width = width
            self.height = height
            self.color = color
            self.rect = pygame.Rect(pos[0]-width/2,pos[1]-height/2,width,height)
            self.remove = False
        def update(self):
            end_x = self.end_x
            end_y = self.end_y
            delta_x = float(end_x-self.start_x)
            delta_y = float(end_y-self.start_y)

            distance = math.sqrt(delta_x*delta_x + delta_y*delta_y)
            if distance == 0:
                distance = 1
            self.rect.centerx = self.start_x + delta_x / distance *self.step
            self.rect.centery = self.start_y + delta_y / distance *self.step

            if self.rect.right < (0):
                self.remove = True
            if self.rect.left > (W):
                self.remove = True
            if self.rect.bottom < (0):
                self.remove = True
            if self.rect.top > (H):
                self.remove = True
            self.step += 10
            return self.remove
        def draw(self, screen):
            pygame.draw.ellipse(screen, self.color, self.rect)

    class Enemy(object):
        def __init__(self, pos, direction, width=20, height=20, color=BLUE):
            self.step = 0
            self.start_x = pos[0]
            self.start_y = pos[1]
            self.width = width
            self.height = height
            self.color = color_list[random.randint(0,len(color_list)-1)]
            self.direction = direction
            self.rect = pygame.Rect(pos[0]-width/2,pos[1]-height/2,width,height)
            self.remove = False
            #printself.rect.center
        def update(self):
            delta = 2
            if self.rect.center == (self.start_x,H*5/6):
                self.direction = 'right'
            if self.rect.center == (W*13/16,H*5/6):
                self.direction = 'up'
            if self.rect.center == (W*13/16,(-1*self.width/2)):
                self.remove = True
                #global escape_count
                #escape_count += 1
                
            if self.direction == 'down':
                self.rect.centery += delta
            else:
                if self.direction == 'up':
                    self.rect.centery -= delta
                else:
                    if self.direction == 'left':
                        self.rect.centerx -= delta
                    else:
                        if self.direction == 'right':
                            self.rect.centerx += delta

            if self.rect.right < (0):
                self.remove = True
            if self.rect.left > (W):
                self.remove = True
            if self.rect.bottom < (0):
                self.remove = True
            if self.rect.top > (H):
                self.remove = True
            return self.remove
                
        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)


        

    #bullet = pygame.Rect(W/4, H/4, 40, 40)
    #tower = pygame.Rect(W/2-20, H/2-20, 40, 40)

    escape_count = 0
    kill_count = 0
    bullets = []
    bullet_removal = []
    enemies = []
    enemy_removal = []
    towers = []
    game = True
    bullet_timer_1 = time.time()
    enemy_timer_1 = time.time()

    #bullets.append(Bullet(tower.center,(800,300)))
    #towers.append(Tower((W/2,H/2)))

    ################################################################

    while game == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONUP:
                towers.append(Tower(event.pos,1))

                    
        for item in towers:
            shoot_check = item.check()
            if shoot_check:
                item.shoot()
            
##        bullet_timer_2 = time.time()
##        if (bullet_timer_2-bullet_timer_1) >= 5:#.5:
##            if len(enemies) >= 1:
##                target = enemies[random.randint(0,len(enemies)-1)]
##                chance = random.randint(0,3)
##                if chance == 0:
##                    if target.direction == 'down':
##                        x_var = target.rect.centerx
##                        y_var = target.rect.centery + 40
##                    if target.direction == 'right':
##                        x_var = target.rect.centerx + 40
##                        y_var = target.rect.centery
##                    if target.direction == 'up':
##                        x_var = target.rect.centerx
##                        y_var = target.rect.centery - 40
##                if chance >= 1:
##                    x_var = random.randint(-50,50) + target.rect.centerx
##                    y_var = random.randint(-50,50) + target.rect.centery
##            else:
##                x_var = random.randint(0,W)
##                y_var = random.randint(0,H)
##            bullets.append(Bullet(tower.center,(x_var,y_var)))
##            bullet_timer_1 = time.time()

        enemy_timer_2 = time.time()
        if (len(enemies) < 100) & (enemy_timer_2-enemy_timer_1 > .4):
            enemies.append(Enemy((W*3/16,0),'down'))
            enemy_timer_1 = time.time()
        
        Surface.fill(BLACK)

        #pygame.draw.rect(Surface, GREEN, tower)

        for item in towers:
            item.draw(Surface)

        for item in enemies:
            remove_bool = item.update()
            item.draw(Surface)
            if remove_bool:
                enemy_removal.append(item)
                escape_count += 1


        for item in bullets:
            for e in enemies:
                if item.rect.colliderect(e.rect):
                    enemy_removal.append(e)
                    bullet_removal.append(item)
                    kill_count += 1
            remove_bool = item.update()
            item.draw(Surface)
            if remove_bool:
                bullet_removal.append(item)
                
        for item in bullet_removal:
            try:
                bullets.remove(item)
            except:
                continue
        bullet_removal = []

        for item in enemy_removal:
            try:
                enemies.remove(item)
                #enemies.append(Enemy((W/8,0)))
                #enemy_timer_1 = time.time()
            except:
                continue
        enemy_removal = []
        
            #pygame.draw.ellipse(Surface, RED, bullet, width=0)

        #pygame.draw.circle(Surface, WHITE, (3*W/4,3*H/4),30)
        #pygame.draw.rect(Surface, GREEN, tower)
        text_print('Escaped: ' + str(escape_count), WHITE, BLACK, 0, 0)
        text_print('Killed: ' + str(kill_count), WHITE, BLACK, 0, 20)
        

        pygame.display.flip()
        mainClock.tick(1000)

if __name__=='__main__':
    selection = start()

    if selection == 'main':
        main()
    
