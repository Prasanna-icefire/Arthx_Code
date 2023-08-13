#import pygame and initialize the pygame engine.
import pygame
import random
#initialize pygame
pygame.init()
#creates a blank window of width 640 pixels and height 480 pixels.
#Window :top left corner is (0, 0), right bottom corner is (640,480).
screen = pygame.display.set_mode((640,480))
#To set the name of our window to “Shapes”
pygame.display.set_caption("Shapes!!")
# Coordinates
x,x2 = 40,590
y,y2 = 180,180
bx = 320
by = 240
speed = 0.2
speedy = 0
# Colors
pure_red = (255, 0, 0)
pure_blue = (0, 0, 255)
pure_green = (0, 255, 0)
pink = (175, 0, 175)
orange = (240, 100, 0)
black = (0,0,0)
white = (255,255,255)
# Flag Variables
up = 0
down = 0
w = 0
s = 0
# Score Variables
scoreA = 0
scoreB = 0
# Define Draw Text Function
def show_text(msg,x,y,color):
    fontobj = pygame.font.SysFont("freesans",32)
    msgobj = fontobj.render(msg,False,color)
    screen.blit(msgobj,(x,y))
#The Game Loop”
while True:
    #Most of our game logic goes here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up = 1
            if event.key == pygame.K_DOWN:
                down = 1
            if event.key == pygame.K_w:
                w = 1
            if event.key == pygame.K_s:
                s = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = 0
            if event.key == pygame.K_DOWN:
                down = 0
    if up == 1:
        y-=0.2
    if down == 1:
        y+=0.2
    y2 = by
    # Restrict paddles from going out of bounds
    if y < 0:
        y = 0
    if y > 480-100:
        y = 380
    if y2 < 0:
        y2 = 0
    if y2 > 480-100:
        y2 = 380

    # Make ball move
    bx += speed
    if bx >= x2 and by >= y2 and by <= y2+100:
        speed = -speed
        speedy = random.uniform(-0.5,0.5)
    if bx <= x and by >= y and by <= y+100:
        speed = -speed
        speedy = random.uniform(-0.5,0.5)
    by += speedy
    if by >= 480 or by <= 0:
        speedy = -speedy
    # Reset ball position
    if bx >= 640:
        bx = 320
        by = 240
        speed = 0.2
        speedy = 0
        scoreA+=1
    if bx <= 0:
        bx = 320
        by = 240
        speed = 0.2
        speedy = 0
        scoreB += 1

    
    screen.fill(black)
    pygame.draw.rect(screen, pure_red,(x,y,15,100,), 0, 0)
    pygame.draw.rect(screen, pure_red,(x2,y2,15,100,), 0, 0)
    pygame.draw.circle(screen, white, (bx,by), 10,0)
    show_text(f"{scoreA}:{scoreB}",300,0,white)
    pygame.display.update()