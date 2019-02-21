import pygame
import os

# the readFile and the writeFile funcitons are from the course website 
# scores mode
class Scores(object):

# returns a list of past scores
    def getNumList(self,list):
        new=[]
        for i in range(len(list)):
            num=int(list[i][:-1])
            new.append(num)
        return new

# loads and configures text    
    def __init__(self,currentHighScore):
        self.backMenu=False
        self._keys = dict()
        self.scoreString=self.readFile('scores.txt')
        self.scoreList=self.getScores('scores.txt')
        self.scoreList=self.getNumList(self.scoreList)
        self.font=pygame.font.SysFont("Comic Sans MS", 70)
        self.subFont=pygame.font.SysFont("Comic Sans MS", 40)
        self.miniFont=pygame.font.SysFont("Comic Sans MS", 25)
        self.done=self.miniFont.render("DONE", False, (0, 0, 0))
        self.doneCoord=(530,372)
        self.title=self.font.render("TOP SCORES",False,(0,0,0))
        self.image = pygame.image.load('images/ufo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(80,80))
        self.mask=pygame.mask.from_surface(self.image)
        self.flag = pygame.image.load('images/flag.png').convert_alpha()
        self.flag = pygame.transform.scale(self.flag,(50,50))

# reads the score file        
    def readFile(self,path):
        with open(path, "rt") as f:
            return f.read()

# writes in the score file            
    def writeFile(self,path,contents):
        self.scoreString=self.readFile(path)
        with open(path,"wt") as f:
            f.write(self.scoreString+contents)

# returns each line of the score file            
    def getScores(self,path):
        with open(path,"rt") as f:
            return f.readlines()

# configures the score list to be drawn on screen           
    def drawList(self):
        self.scoreList=self.getScores('scores.txt')
        self.scoreList=self.getNumList(self.scoreList)
        self.scoreList.sort()
 
# keeps track of mouse clicks on buttons to navigate pages    
    def mousePressed(self, x, y):
        doneButton=self.done.get_rect()
        doneButton.move_ip(self.doneCoord)
        if doneButton.collidepoint(x,y):
            self.backMenu=True
                
# keeps track of keys pressed to navigate pages        
    def keyPressed(self, keyCode, modifier):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.backMenu=True
 
    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos))
            elif event.type == pygame.KEYDOWN:
                self._keys[event.key] = True
                self.keyPressed(event.key, event.mod)
            
    def redrawAll(self,screen):
        screen.fill((255,255,255))
        screen.blit(self.image,(480,5))
        screen.blit(self.flag,(530,3))
        screen.blit(self.done,self.doneCoord)
        screen.blit(self.title,(10,10))
        for score in range(0,5):
            image=self.subFont.render("%d     %d" % (score+1,\
                self.scoreList[-1-score]),False,(0,0,0))
            screen.blit(image,(80,110+score*50))
        for score in range(5,10):
            image=self.subFont.render("%d     %d" % (score+1,\
                self.scoreList[-1-score]),False,(0,0,0))
            if score==9:
                screen.blit(image,(355,110+(score-5)*50))
            else:
                screen.blit(image,(370,110+(score-5)*50))
        
        