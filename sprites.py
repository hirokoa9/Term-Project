import pygame
import random
import math

# sprite groups called in game play mode
class Missile(pygame.sprite.Sprite):

# loads and configures missile images    
    def __init__(self,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('missile.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(60,20))
        self.y=y
        self.angle=0
        self.direction=direction
        self.mask=pygame.mask.from_surface(self.image)
        self.explosion=False
        if direction==1:
            self.x=-50
            self.xMove=5
            self.yMove=0
            self.rect=self.image.get_rect()
            self.rect.move_ip(self.x,self.y)
        else:
            self.image = pygame.transform.flip(self.image,True,False)
            self.x=600
            self.xMove=-5
            self.yMove=0
            self.rect=self.image.get_rect()
            self.rect.move_ip(self.x,self.y)

# moves missile to follow ufo and checks for collision with ufo,
# pops if off screen          
    def update(self, player,beam,explosion,time):
        if time%8==0:
            if self.direction==1:
                self.xMove=int((player.x-self.x)/\
                    ((((player.x-self.x)**2+(self.y-player.y)**2)**0.5)/5))
                self.yMove=int((player.y-self.y)/\
                    ((((player.x-self.x)**2+(self.y-player.y)**2)**0.5)/5))
                self.angle=((math.atan2(self.yMove,self.xMove)*180)/math.pi)
            else:
                self.xMove=int((player.x-self.x)/\
                    ((((player.x-self.x)**2+(self.y-player.y)**2)**0.5)/5))
                self.yMove=int((player.y-self.y)/\
                    ((((player.x-self.x)**2+(self.y-player.y)**2)**0.5)/5))
                self.angle=((math.atan2(self.yMove,self.xMove)*180)/math.pi)
        if self.direction==1:
            if self.angle<player.difficulty and self.angle>-player.difficulty \
                and abs(self.x-player.x)>80:
                self.x+=self.xMove
                self.y+=self.yMove
                self.rect.move_ip(self.xMove,self.yMove)
            else:
                self.x+=5
                self.rect.move_ip(5,0)
            if self.x>600:
                self.kill()
        else:
            if self.angle>(180-player.difficulty) or \
                self.angle<-(180-player.difficulty) and abs(self.x-player.x)>80:
                self.x+=self.xMove
                self.y+=self.yMove
                self.rect.move_ip(self.xMove,self.yMove)
            else:
                self.x-=5
                self.rect.move_ip(-5,0)
            if self.x<-50:
                self.kill()
        if player.invincible==False:
            if pygame.sprite.collide_mask(player, self) != None:
                self.kill()
                player.livesLeft-=1
                pygame.mixer.Channel(1).play(explosion)
                player.killed=time
                
class UFO(pygame.sprite.Sprite):
    
# loads and configures ufo image
    def __init__(self,lives,x=260,y=160):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.image = pygame.image.load('ufo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect=self.image.get_rect()
        self.rect.move_ip(self.x,self.y)
        self.mask=pygame.mask.from_surface(self.image)
        self.livesLeft=lives
        self.score=0
        self.gauge=0
        self.speed=1
        self.killed=0
        self.difficulty=1
        self.invincible=False

# moves ufo image        
    def update(self, x=0, y=0):
        self.x+=x
        self.y+=y
        self.rect.move_ip(x,y)
        
class Beam(pygame.sprite.Sprite):
    
# loads and configures beam image    
    def __init__(self,x=230,y=240):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.image = pygame.image.load('beam.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.rect.move_ip(self.x,self.y)

# moves ufo beam so that it follows ufo        
    def update(self, x=0, y=0):
        self.x+=x
        self.y+=y
        self.rect.move_ip(x,y)
        
class Human(pygame.sprite.Sprite):
    
# loads and configures the targets
    def __init__(self,xCoord,player):
        pygame.sprite.Sprite.__init__(self)
        self.size=(35,35)
        self.ySize=35
        self.windowHeight=400
        self.ground=10
        self.image = pygame.image.load('stick_figure.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.size))
        self.mask=pygame.mask.from_surface(self.image)
        self.x=xCoord
        self.origY=self.windowHeight-self.ground-self.ySize
        self.y=self.windowHeight-self.ground-self.ySize
        self.rect=self.image.get_rect()
        self.rect.move_ip(self.x,self.y)
        self.speed=2+player.speed

# moves target and checks for collision, pops if off screen    
    def update(self,isBeam,player,beam,sound):
        self.x-=2
        self.rect.move_ip(-2,0)
        if self.x<-20:
            self.kill()
        if isBeam:
            if pygame.sprite.collide_mask(beam, self) != None:
                self.y-=self.speed
                self.rect.move_ip(0,-self.speed)
            else:
                if self.y<self.origY:
                    self.y+=4
                    self.rect.move_ip(0,4)
            if pygame.sprite.collide_mask(player, self) != None:
                self.kill()
                pygame.mixer.Channel(2).play(sound)
                player.score+=10
                player.gauge+=4
                if player.gauge%100==0:
                    player.speed+=1
                    player.difficulty+=25
        else:
            if self.y<self.origY:
                self.y+=4
                self.rect.move_ip(0,4)
        
class House(pygame.sprite.Sprite):
    
# loads and configures the targets
    def __init__(self,xCoord,player):
        pygame.sprite.Sprite.__init__(self)
        self.windowHeight=400
        self.ground=10
        self.size=(50,50)
        self.ySize=50
        self.image = pygame.image.load('house.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,self.size)
        self.mask=pygame.mask.from_surface(self.image)
        self.x=xCoord
        self.origY=self.windowHeight-self.ground-self.ySize
        self.y=self.windowHeight-self.ground-self.ySize
        self.rect=self.image.get_rect()
        self.rect.move_ip(self.x,self.y)
        self.speed=1+player.speed
        
# moves target and checks for collision, pops if off screen
    def update(self,isBeam,player,beam,sound):
        self.x-=2
        self.rect.move_ip(-2,0)
        if self.x<-20:
            self.kill()
        if isBeam:
            if pygame.sprite.collide_mask(beam, self) != None:
                self.y-=self.speed
                self.rect.move_ip(0,-self.speed)
            else:
                if self.y<self.origY:
                    self.y+=4
                    self.rect.move_ip(0,4)
            if pygame.sprite.collide_mask(player, self) != None:
                self.kill()
                pygame.mixer.Channel(3).play(sound)
                player.score+=50
                player.gauge+=4
                if player.gauge%100==0:
                    player.speed+=1
                    player.difficulty+=25
        else:
            if self.y<self.origY:
                self.y+=4
                self.rect.move_ip(0,4)
        
class Building(pygame.sprite.Sprite):
    
# loads and configures the targets
    def __init__(self,xCoord,player):
        pygame.sprite.Sprite.__init__(self)
        self.windowHeight=400
        self.ground=10
        self.size=(40,65)
        self.ySize=65
        self.image = pygame.image.load('building.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,self.size)
        self.mask=pygame.mask.from_surface(self.image)
        self.x=xCoord
        self.origY=self.windowHeight-self.ground-self.ySize
        self.y=self.windowHeight-self.ground-self.ySize
        self.rect=self.image.get_rect()
        self.rect.move_ip(self.x,self.y)
        self.speed=0+player.speed
    
# moves target and checks for collision, pops if off screen
    def update(self,isBeam,player,beam,sound):
        self.x-=2
        self.rect.move_ip(-2,0)
        if self.x<-20:
            self.kill()
        if isBeam:
            if pygame.sprite.collide_mask(beam, self) != None:
                self.y-=self.speed
                self.rect.move_ip(0,-self.speed)
            else:
                if self.y<self.origY:
                    self.y+=6
                    self.rect.move_ip(0,6)
            if pygame.sprite.collide_mask(player, self) != None:
                self.kill()
                pygame.mixer.Channel(4).play(sound)
                player.score+=100
                player.gauge+=4
                if player.gauge%100==0:
                    player.speed+=1
                    player.difficulty+=25
        else:
            if self.y<self.origY:
                self.y+=4
                self.rect.move_ip(0,4)
        
        