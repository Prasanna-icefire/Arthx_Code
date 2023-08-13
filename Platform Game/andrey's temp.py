import pygame
from pygame.locals import *
black = (0,0,0)
import random
class circle():
     radius=20 # To create a class variable, you need to add this variable outside the init function
     def __init__(self,x,y):
          
          self.x=x
          self.y=y
0
obj=[]
for n in range(0,10,1):
     circle_object=circle(random.randint(20,580),random.randint(20,580))
     obj.append(circle_object)

         
          

def show_text(msg, x, y, color, size):
        fontobj= pygame.font.SysFont("freesans", size)
        msgobj = fontobj.render(msg,False,color)
        screen.blit(msgobj,(x, y))

pygame.init()
screen=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()

while True:
    
    screen.fill(black)
    for event in pygame.event.get():
        if event.type==KEYDOWN:
             if event.key==K_UP:
               circle.radius=circle.radius+20
             if event.key==K_DOWN:
               circle.radius=circle.radius-20
        if event.type==QUIT:
            pygame.quit()
            exit()
    for cir in obj:
        pygame.draw.circle(screen,(255,255,255),(cir.x,cir.y),cir.radius)
    clock.tick(30)
    pygame.display.update()
    
