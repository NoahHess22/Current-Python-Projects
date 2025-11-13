import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption('Platformer')
width,height=1000,800
fps=60
player_velocity=5
window=pygame.display.set_mode((width,height))

def flip(sprites):
    return [pygame.transform.flip(sprite,True,False) for sprite in sprites]
def load_sprite_sheets(dir1,dir2,width,height,direction=False):
    path=join('assets',dir1,dir2)
    images=[f for f in listdir(path) if isfile(join(path,f))]
    all_sprites={}
    for image in images:
        sprite_sheet=pygame.image.load(join(path,image)).convert_alpha()
        sprites=[]
        for i in range(sprite_sheet.get_width() // width):
            surface=pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect=pygame.Rect(i*width,0,width,height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace('.png','')+'_right']=sprites
            all_sprites[image.replace('.png','')+'_left']=flip(sprites)
        else:
            all_sprites[image.replace('.png','')]=sprites
    return all_sprites

def get_block(size):
    path=join('assets','Terrain','Terrain.png')
    image=pygame.image.load(path).convert_alpha()
    surface=pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect=pygame.Rect(96,0,size,size)
    surface.blit(image,(0,0),rect)
    return pygame.transform.scale2x(surface)

class player(pygame.sprite.Sprite):
    color=(255,0,0)
    gravity=1
    sprites=load_sprite_sheets('MainCharacters','PinkMan',32,32,True)
    animation_delay=5


    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        self.direction='left'
        self.animation_count=0
        self.fall_count=0
        self.jump_count=0
        self.hit=False
        self.hit_count=0

    def make_hit(self):
        self.hit=True
        self.hit_count=0
    
    def jump(self):
        self.y_vel= -self.gravity*8
        self.animation_count=0
        self.jump_count+=1
        if self.jump_count==1:
            self.fall_count=0
    def move(self,dx,dy):
        self.rect.x+=dx
        self.rect.y+=dy
    def move_left(self,vel):
        self.x_vel=-vel
        if self.direction!='left':
            self.direction='left'
            self.animation_count=0
    def move_right(self,vel):
        self.x_vel=vel
        if self.direction!='right':
            self.direction='right'
            self.animation_count=0

    def loop(self,fps):
        self.y_vel+=min(1,(self.fall_count/fps)*self.gravity)
        self.move(self.x_vel,self.y_vel)

        if self.hit:
            self.hit_count+=1
            if self.hit_count>fps*2:
                self.hit=False
                self.hit_count=0
        self.fall_count+=1
        self.update_sprite()
    
    def landed(self):
        self.fall_count=0
        self.y_vel=0
        self.jump_count=0
    
    def hit_head(self):
        self.count=0
        self.y_vel*=-1
    
    def update_sprite(self):
        sprite_sheet='idle'
        if self.hit:
            sprite_sheet='hit'
        if self.y_vel<0:
            if self.jump_count==1:
                sprite_sheet='jump'
            elif self.jump_count==2:
                sprite_sheet='double_jump'
        elif self.y_vel>self.gravity * 20:
            sprite_sheet='fall'
        elif self.x_vel!=0:
            sprite_sheet='run'
        sprite_sheet_name=sprite_sheet+'_'+self.direction
        sprites=self.sprites[sprite_sheet_name]
        sprite_index=(self.animation_count//self.animation_delay)%len(sprites)
        self.sprite=sprites[sprite_index]
        self.animation_count+=1
        self.update()
    
    def update(self):
         self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
         self.mask=pygame.mask.from_surface(self.sprite)

    def draw(self,window,offset_x):
        window.blit(self.sprite,(self.rect.x-offset_x,self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
        self.image=pygame.Surface((width,height),pygame.SRCALPHA)
        self.width=width
        self.height=height
        self.name=name
    def draw(self,window,offset_x):
        window.blit(self.image,(self.rect.x-offset_x,self.rect.y))

class Block(Object):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,size)
        block=get_block(size)
        self.image.blit(block,(0,0))
        self.mask=pygame.mask.from_surface(self.image)

class Fire(Object):
    animation_delay=3
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,'fire')
        self.fire=load_sprite_sheets('Traps','Fire',width,height)
        self.image=self.fire['off'][0]
        self.mask=pygame.mask.from_surface(self.image)
        self.animation_count=0
        self.animation_name='off'
    def on(self):
        self.animation_name='on'
    def off(self):
        self.animation_name='off'
    def loop(self):
        sprites=self.fire[self.animation_name]
        sprite_index=(self.animation_count//self.animation_delay)%len(sprites)
        self.image=sprites[sprite_index]
        self.animation_count+=1
        self.rect=self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask=pygame.mask.from_surface(self.image)
        
        if self.animation_count//self.animation_delay> len(sprites):
            self.animation_count=0

def get_background(name):
    image=pygame.image.load(join('assets','Background',name))
    _,_,w,h=image.get_rect()
    tiles=[]
    for i in range(width // w+1):
        for j in range(height // h+1):
            pos=(i*w,j*h)
            tiles.append(pos)
    return tiles,image

def draw(window,background,bg_image,player,objects,offset_x):
    for tile in background:
        window.blit(bg_image,tile)
    player.draw(window,offset_x)
    for obj in objects:
        obj.draw(window,offset_x)
    pygame.display.update()

def handle_vertical_collision(player,objects,dy):
    collided_objects=[]
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy>0:
                player.rect.bottom=obj.rect.top
                player.landed()
            elif dy<0:
                player.rect.top=obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects

def collide(player,objects,dx):
    player.move(dx,0)
    player.update()
    collided_objects=None
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            collided_objects=obj
            break
    player.move(-dx,0)
    player.update()
    return collided_objects

def handle_movement(player,objects):
    keys = pygame.key.get_pressed()
    player.x_vel=0
    collide_left=collide(player,objects,-player_velocity*2)
    collide_right=collide(player,objects,player_velocity*2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(player_velocity)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(player_velocity)

    vertical_collide=handle_vertical_collision(player,objects,player.y_vel)
    to_check=[collide_left,collide_right,*vertical_collide]
    for obj in to_check:
        if obj and obj.name=='fire':
            player.make_hit()



def main(window):
    clock=pygame.time.Clock()
    background,bg_image=get_background('Gray.png')
    
    block_size=96
    player1 =player(100,100,50,50)
    fire=Fire(100,height-block_size-64,16,32)
    fire.on()
    floor=[Block(i*block_size,height-block_size,block_size) for i in range(-width//block_size,(width*2)//block_size)]
    offset_x=0
    scroll_area_width=200
    objects=[*floor,Block(0,height-block_size*2,block_size),Block(block_size*3,height-block_size*4,block_size)
    ,fire]

    run=True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player1.jump_count<2:
                    player1.jump()
        
        player1.loop(fps)
        fire.loop()
        handle_movement(player1,objects)
        draw(window,background,bg_image,player1,objects,offset_x)
        if (player1.rect.right - offset_x >= width-scroll_area_width and player1.x_vel>0) or ((player1.rect.left - offset_x <= scroll_area_width) and player1.x_vel <0):
            offset_x+=player1.x_vel

    pygame.quit()
    quit()

if __name__ == '__main__':
    main(window)