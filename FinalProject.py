#Noah Hess
#11/7/25
#Ball Bounce Game
import pygame
import random
import os
import math
pygame.init()
width,height=800,600
fps=60
window=pygame.display.set_mode((width,height))
player_velocity=10

class Ball:
    gravity=500
    def __init__(self,x,y,radius,color):
        self.rect=pygame.Rect(x-radius,y-radius,radius*2,radius*2)
        self.x=x
        self.y=y
        self.gravity=Ball.gravity
        self.radius=radius
        self.color=color
        self.x_vel=0
        self.y_vel=0
    def loop(self,fps):
        dt = 1.0/fps if fps>0 else 0.0
        self.y_vel+=self.gravity*dt
        self.y+=self.y_vel*dt
        self.x+=self.x_vel*dt
        self.rect.x=int(self.x - self.radius)
        self.rect.y=int(self.y - self.radius)
    def move(self,dx,dy):
        self.rect.x+=dx
        self.rect.y+=dy
    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.rect.x+self.radius,self.rect.y+self.radius),self.radius)

class playerPlatform:
    def __init__(self,x,y,width,height):
        self.rect=pygame.Rect(x,y,width,height)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.x_vel=0
        self.mask=None
        self.hit=False
        self.hit_count=0
    def make_hit(self):
        self.hit=True
        self.hit_count+=1
    def loop(self,fps):
        #Update x value based on x_vel
        self.move(self.x_vel)
    def move(self,dx):
        self.rect.x+=dx
    def move_left(self,vel):
        self.x_vel=-vel
    def move_right(self,vel):
        self.x_vel=vel
    def update(self):
         self.rect=self.get_rect(topleft=(self.rect.x,self.rect.y))
         self.mask=pygame.mask.from_surface(self.sprite)
    def draw(self,window):
        pygame.draw.rect(window,(255,255,255),self.rect,)

def player_collision(player,ball):
    #Make the ball bounce off the player in the opposite direction
    if ball.rect.colliderect(player.rect):
        ball.y_vel=-abs(ball.y_vel)

        ball_center=ball.rect.centerx
        player_center=player.rect.centerx
        diff=ball_center-player_center
        percentdiff=diff/(player.rect.width/2)
        ball.x_vel=percentdiff*200
        ball.y=player.rect.y-ball.radius
        player.hit_count+=1
def border_collision(ball,width,height):
    #The left wall
    if ball.rect.left<=0:
        ball.rect.left=0
        ball.x=ball.rect.x+ball.radius
        ball.x_vel=abs(ball.x_vel)
    #The right wall
    elif ball.rect.right>=width:
        ball.rect.right=width
        ball.x=ball.rect.x+ball.radius
        ball.x_vel=-abs(ball.x_vel)
    #Top wall
    if ball.rect.top<=0:
        ball.rect.top=0
        ball.y=ball.rect.y+ball.radius
        ball.y_vel=abs(ball.y_vel)
def player_border(player,width):
    if player.rect.right<0:
        player.rect.left=width
    elif player.rect.left>width:
        player.rect.right=0    


def playermovement(player,objects):
    keys=pygame.key.get_pressed()
    player.x_vel=0
    if keys[pygame.K_LEFT]:
        player.move_left(player_velocity)
    elif keys[pygame.K_RIGHT]:
        player.move_right(player_velocity)

def draw(window,ball,player):
    window.fill((0,255,255))
    ball.draw(window)
    player.draw(window)
    pygame.display.update()

if __name__=='__main__':
    run=True
    clock=pygame.time.Clock()
    ball=Ball(400,300,15,(155,30,200))
    player=playerPlatform(350,550,100,20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        clock.tick(fps)
        
        playermovement(player,[])
        player.loop(fps)
        player_border(player,width)
        ball.loop(fps)
        player_collision(player,ball)
        border_collision(ball,width,height)
        draw(window,ball,player)

    
    pygame.quit()