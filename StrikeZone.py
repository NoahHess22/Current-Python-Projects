import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

#Create a display window
pygame.init()
pygame.display.set_caption('Strike Zone')
width,height=1000,800
fps=60
window=pygame.display.set_mode((width,height))

#Colors
white=(255,255,255)
black=(0,0,0)
green=(100,200,150)


class baseball:
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y
        self.radius=15
        self.color=white
        self.x_vel=0
        self.y_vel=0
        self.gravity=0.5
        self.hit_strength=-15
        self.on_ground=False
        self.bounced=False
    
    def update(self,ground_y):
        if not self.on_ground:
            self.y_vel+=self.gravity
            self.y+=self.y_vel
            self.x+=self.x_vel
        if self.y+self.radius>=ground_y:
            self.y=ground_y-self.radius
            if not self.bounced and self.y_vel>1:
                self.y_vel*=-0.5
                self.has_bounced=True
                self.on_ground=False
            else:
                self.y_vel=0
                self.on_ground=True
                self.x_vel=0
    
    def hit(self):
        if self.on_ground:
            self.y_vel=self.hit_strength
            self.x_vel=random.uniform(-6,6)
            self.on_ground=False
            self.has_bounced=False
    
    def draw(self,window):
        pygame.draw.circle(window,self.color,(int(self.x),int(self.y)),self.radius)

    def off_screen(self):
        return self.y>height+100 or self.x<-200 or self.x>width+200
    

class strikezone:
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y
        self.width=120
        self.height=30
        self.color=black
        self.rect=pygame.Rect(self.x-self.width//2,self.y-self.height//2,self.width,self.height)

    def draw(self,window):
        pygame.draw.rect(window,self.color,self.rect)


def draw(window,ball,plate):
    window.fill(green)
    plate.draw(window)
    ball.draw(window)
    pygame.display.update()




def main(window):
    clock=pygame.time.Clock()
    ball=baseball(width//2,100)
    plate=strikezone(width//2,height-80)
    ground_y=height-50
    
    run=True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                ball.hit()
        ball.update(ground_y)
        if ball.y<-50 or ball.x<-100 or ball.x>width+100:
            ball=baseball(width//2,100)

        draw(window,ball,plate)
    pygame.quit()
if __name__=='__main__':
    main(window)