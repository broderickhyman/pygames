import pygame, sys, time, math, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
all_fonts = pygame.font.get_fonts()
basicFont = pygame.font.SysFont('arial', 20)

W = 700
H = 500

Surface = pygame.display.set_mode((W,H), 0, 32)
pygame.display.set_caption('Learn To Fly')

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

class Star(object):
    def __init__(self, x, y, width=10, height=10):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = WHITE#color_list[random.randint(0,len(color_list)-1)]
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
    def update(self, delta_x, delta_y):
        self.x -= delta_x
        self.y += delta_y
        if self.y > H + 75:
            self.y -= H + 100
        else:
            if self.y < -75:
                self.y += H + 100
        if self.x < (0-self.width):
            self.x += W + 100
        self.rect.center = (self.x, self.y)
        
#        self.rect.right -= math.cos(math.radians(degree+6))*speed
#        self.rect.bottom += math.sin(math.radians(degree+6))*speed
    def draw(self):
        pygame.draw.rect(Surface, self.color, self.rect)

game = True
plane = pygame.image.load('plane.png')
#plane2 = pygame.transform.rotate(plane, 90)
degree = 0
turn_left = False
turn_right = False
free_falling = False
stars = []
#star_removal = []
#star = pygame.Rect(0, 0, 20, 20)
#star.center = (W*3/4,H/2)
frame_counter = 0
fps_timer = time.time()
fps = 0
speed = 10
star_spawner = time.time()
rows = H/100 + 2
columns = W/100 + 1
change_y = 0
falling_y = change_y
altitude = 500 * 0
pause = False
for i in range(0,rows):
    for j in range(0,columns):
        stars.append(Star(j * 100 - 50, i *100 + 50))

while game == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT:
                turn_right = False
            if event.key == K_LEFT:
                turn_left = False
            if event.key == K_p:
                if pause:
                    pause = False
                else:
                    pause = True
                
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                turn_right = True
                turn_left = False
            if event.key == K_LEFT:
                turn_left = True
                turn_right = False
    

    if pause == False:
        change_x = math.cos(math.radians(degree))*speed
        if change_x < 5:
            if falling == False:
                falling = True
                change_y = 0
                fall_time = time.time()
        else:
            falling = False
            
        if falling == False:
            change_y = math.sin(math.radians(degree))*speed
            if falling_y < change_y:
                change_y = falling_y + .1
                falling_y = change_y
            else:
                falling_y = 100
        else:
            falling_y = -2 * (time.time()-fall_time)
            change_y = falling_y

        altitude += change_y
        for item in stars:
            star_check = item.update(change_x,change_y)
        
        if turn_right:
            degree -= .5
            #print degree
        if turn_left:
            degree += .5
            #print degree
        if degree < -70:
            degree = -70
        if degree > 70:
            degree = 70
            #print degree

        if falling:
            speed += -1 * float(degree) /1000
        else:
            speed += -1 * float(degree) /1000        
        if speed < 0:
            speed = 0
    
    plane2 = pygame.transform.rotate(plane, degree)

    Surface.fill(BLACK)
    Surface.blit(plane2,(W/2-plane2.get_width()/2,H/2-plane2.get_height()/2))

    for item in stars:
        item.draw()
    
    frame_counter += 1
    time_dif = time.time() - fps_timer
    if time_dif > .1:
        fps = frame_counter / time_dif
        frame_counter = 0
        fps_timer = time.time()

    text_print('FPS:' + str(int(fps)),GREEN,BLACK,0,H-30)
    text_print('Speed:' + str(speed),GREEN,BLACK,0,0)
    text_print('Degree:' + str(degree),GREEN,BLACK,0,25)
    text_print('Delta X:' + str(change_x),GREEN,BLACK,0,50)
    text_print('Delta y:' + str(change_y),GREEN,BLACK,0,75)
    text_print('Falling y:' + str(falling_y),GREEN,BLACK,0,100)
    text_print('Altitude:' + str(altitude/500),GREEN,BLACK,0,125)
    #pygame.draw.rect(Surface, BLUE, star)
    
    pygame.display.flip()
    mainClock.tick(100)
