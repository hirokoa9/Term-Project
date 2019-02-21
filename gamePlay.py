import pygame
import random
from sprites import Missile
from sprites import UFO
from sprites import Beam
from sprites import Human
from sprites import House
from sprites import Building

# game play mode
class Game(object):
    
# loads the images needed for game
    def images(self):
        self.heart = pygame.image.load('images/Heart.png').convert_alpha()
        self.heart = pygame.transform.scale(self.heart,(30,30))
        self.explode=pygame.image.load('images/explosion.png').convert_alpha()
        self.explode=pygame.transform.scale(self.explode,(80,80))

# loads the sounds needed for game    
    def sounds(self):
        self.explosion=pygame.mixer.Sound('sound/explosion.ogg')
        self.gameover=pygame.mixer.Sound('sound/gameover.wav')
        self.gameclear=pygame.mixer.Sound('sound/gameclear.wav')
        self.beamSound=pygame.mixer.Sound('sound/ufo.wav')
        self.beamSound.set_volume(0.2)
        self.pickUp=pygame.mixer.Sound('sound/score.wav')
    
    def __init__(self,highScore):
        self.images()
        self.sounds()
        self.player=UFO(3)
        self.gauge=0
        self.score=0
        self.ufoSize=80
        self.highScore=highScore
        self.font=pygame.font.SysFont("Comic Sans MS", 50)
        self.miniFont=pygame.font.SysFont("Comic Sans MS", 25)
        self.life=self.font.render("LIFE", False, (0, 0, 0))
        self.largeFont=pygame.font.SysFont("Comic Sans MS", 140)
        self.text=self.largeFont.render("PAUSED",False,(0,0,0))
        self.textCoords=(100,150)
        self._keys = dict()
        self.gameOver=False
        self.gameClear=False
        self.pause=False
        self.detectP=False
        self.time=0
        self.drawBeam=False
        self.number=0
        self.missileList=pygame.sprite.Group()
        self.humans=pygame.sprite.Group()
        self.houses=pygame.sprite.Group()
        self.buildings=pygame.sprite.Group()
        self.beam=Beam()

# plays bgm
    def playMusic(self):
        pygame.mixer.music.load('sound/gameBGM.ogg')
        pygame.mixer.music.play(-1)

# when called, generates a missile at a random location and adds to sprite group
    def spawnMissiles(self):
        direction=random.randint(0,1)
        yCoord=random.randint(120,290)
        spawn=Missile(yCoord,direction)
        self.missileList.add(spawn)

# generates targets on screen when game starts     
    def setScreen(self):
        if self.time==0:
            for i in range(0,10):
                number=random.randint(1,30)*20
                which=random.randint(1,60)
                person=Human(number,self.player)
                house=House(number,self.player)
                building=Building(number,self.player)
                if which>=30:
                    self.humans.add(person)
                elif which>=10 and which<30:
                    self.houses.add(house)
                else:
                    self.buildings.add(building)
    
# when called, generates targets at random timings and adds to sprite group
    def spawnTargets(self):
        number=random.randint(1,500)
        if number<200:
            person=Human(600,self.player)
            self.humans.add(person)
        if number<300 and number>200:
            house=House(600,self.player)
            self.houses.add(house)
        if number>450:
            building=Building(600,self.player)
            self.buildings.add(building)
    
# checks keys pressed and lifted in order to control ufo and beam    
    def keys(self):
        if self.pause:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_p]:
                if self.detectP==False:
                    if self.pause==False:
                        pygame.mixer.music.pause()
                        self.pause=True
                    else:
                        pygame.mixer.music.unpause()
                        self.pause=False
                self.detectP=True
            if not keys[pygame.K_p]:
                self.detectP=False
        else:
            keys=pygame.key.get_pressed()
            self.speed=5
            if keys[pygame.K_SPACE]:
                if self.player.invincible==False:
                    pygame.mixer.Channel(0).play(self.beamSound,loops=-1)
                    self.drawBeam=True
            if self.drawBeam:
                self.speed=2
            if keys[pygame.K_UP]:
                if self.player.y>65:
                    self.player.update(y=-self.speed)
                    self.beam.update(y=-self.speed)
            if keys[pygame.K_DOWN]:
                if (self.player.y+self.ufoSize)<300:
                    self.player.update(y=self.speed)
                    self.beam.update(y=self.speed)
            if keys[pygame.K_RIGHT]:
                if (self.player.x+self.ufoSize)<600:
                    self.player.update(x=self.speed)
                    self.beam.update(x=self.speed)
            if keys[pygame.K_LEFT]:
                if self.player.x>0:
                    self.player.update(x=-self.speed)
                    self.beam.update(x=-self.speed)
            if not keys[pygame.K_SPACE]:
                self.beamSound.stop()
            if keys[pygame.K_p]:
                if self.detectP==False:
                    if self.pause==False:
                        self.beamSound.stop()
                        pygame.mixer.music.pause()
                        self.pause=True
                    else:
                        pygame.mixer.music.unpause()
                        self.pause=False
                self.detectP=True
            if not keys[pygame.K_p]:
                self.detectP=False

# controls everything dependent on time, including updating sprites and spawning
    def timerFired(self, dt):
        if self.pause:
            pass
        else:
            self.setScreen()
            self.missileList.explosion=False
            self.drawBeam=False
            self.time+=1
            self.number=random.randint(1,10)
            self.keys()
            if self.player.livesLeft<=0:
                self.gameover.play()
                self.gameOver=True
                return
            if self.time%100==0:
                if self.number>3:
                    self.spawnMissiles()
            if self.time%30==0:
                self.spawnTargets()
            self.missileList.update(self.player,self.beam,self.explosion,\
                self.time)
            if self.time%2==0:
                self.humans.update(self.drawBeam,self.player,self.beam,\
                    self.pickUp)
                self.houses.update(self.drawBeam,self.player,self.beam,\
                    self.pickUp)
                self.buildings.update(self.drawBeam,self.player,self.beam,\
                    self.pickUp)
            self.score=self.player.score
            self.gauge=self.player.gauge
            if self.score>self.highScore:
                self.highScore=self.score
            if self.gauge==400:
                self.gameclear.play()
                self.score+=(self.player.livesLeft*500)
                if self.score>self.highScore:
                    self.highScore=self.score
                self.gameClear=True
            if self.player.killed!=0 and self.time<(self.player.killed+45) and \
                self.time>self.player.killed:
                self.beamSound.stop()
                self.player.invincible=True
            else:
                self.player.invincible=False
 
# draws the hearts/lives on the screen
    def drawLife(self,screen):
        if self.player.livesLeft>2:
            screen.blit(self.heart,(180,10))
        if self.player.livesLeft>1:
            screen.blit(self.heart,(140,10))
        if self.player.livesLeft>0:
            screen.blit(self.heart,(100,10))
            
    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass

# draws the game screen    
    def redrawAll(self, screen):
        self.scoreText=self.miniFont.render\
            ("SCORE  %d" % self.score,False,(0,0,0))
        self.highScoreText=self.miniFont.render\
            ("HIGH SCORE  %d" % self.highScore,False,(0,0,0))
        screen.fill((255,255,255))
        if self.player.invincible==False:
            screen.blit(self.player.image,self.player.rect)
        else:
            if self.player.killed!=0 and self.time<(self.player.killed+10)\
                and self.time>self.player.killed:
                screen.blit(self.explode,(self.player.x,self.player.y))
            if self.time%5==0:
                screen.blit(self.player.image,self.player.rect)
        screen.blit(self.life,(10,10))
        screen.blit(self.scoreText,(400,30))
        screen.blit(self.highScoreText,(400,10))
        pygame.draw.rect(screen,(0,0,0),(0,390,600,10))
        pygame.draw.rect(screen,(0,0,0),(100,70,400,20),2)
        pygame.draw.rect(screen,(0,0,0),(100,70,self.gauge,20))
        self.drawLife(screen)
        self.buildings.draw(screen)
        self.houses.draw(screen)
        self.humans.draw(screen)
        self.missileList.draw(screen)
        if self.drawBeam:
            pygame.draw.lines(screen,(0,0,0),False,\
                [(self.player.x+self.ufoSize,self.player.y+self.ufoSize),\
                (self.player.x+self.ufoSize+30,\
                self.player.y+self.ufoSize+190)],4)
            pygame.draw.lines(screen,(0,0,0),False,\
                [(self.player.x-30,self.player.y+self.ufoSize+190),\
                (self.player.x,self.player.y+self.ufoSize)],4)
        if self.pause:
            screen.blit(self.text,(self.textCoords))

                