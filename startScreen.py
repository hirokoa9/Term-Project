import pygame

# start/menu mode
class Start(object):
    
# loads and configures images and texts
    def __init__(self,highScore):
        self.ufo = pygame.image.load('ufo.png').convert_alpha()
        self.person = pygame.image.load('stick_figure.png').convert_alpha()
        self.house = pygame.image.load('house.png').convert_alpha()
        self.missile = pygame.image.load('missile.png').convert_alpha()
        pygame.font.init()
        self.font=pygame.font.SysFont("Comic Sans MS", 70)
        self.subFont=pygame.font.SysFont("Comic Sans MS", 40)
        self.miniFont=pygame.font.SysFont("Comic Sans MS", 30)
        self.title=self.font.render("PLANET INVADER", False, (0, 0, 0))
        self.play=self.subFont.render("PLAY", False, (0, 0, 0))
        self.scores=self.subFont.render("SCORES", False, (0, 0, 0))
        self.exit=self.subFont.render("EXIT",False,(0,0,0))
        self.playCoords=(15,120)
        self.infoCoords=(15,160)
        self.scoresCoords=(15,200)
        self.exitCoords=(15,240)
        self.info=self.subFont.render("HOW TO PLAY", False, (0, 0, 0))
        self.scoreText=self.miniFont.render\
            ("HIGH SCORE %d" % highScore,False, (0, 0, 0))
        self.enterPlay=False
        self.enterHowTo=False
        self.exitGame=False
        self.enterScores=False
        self._keys = dict()

# keeps track of mouse clicks on buttons
    def mousePressed(self, x, y):
        playButton=self.play.get_rect()
        playButton.move_ip(self.playCoords)
        howToButton=self.info.get_rect()
        howToButton.move_ip(self.infoCoords)
        exitButton=self.exit.get_rect()
        exitButton.move_ip(self.exitCoords)
        scoresButton=self.scores.get_rect()
        scoresButton.move_ip(self.scoresCoords)
        if playButton.collidepoint(x,y):
            self.enterPlay=True
        elif howToButton.collidepoint(x,y):
            self.enterHowTo=True
        elif exitButton.collidepoint(x,y):
            self.exitGame=True
        elif scoresButton.collidepoint(x,y):
            self.enterScores=True

    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos))
        
# draws images and text on screen
    def redrawAll(self, screen):
        screen.blit(self.ufo,self.ufo.get_rect())
        screen.blit(self.title,(10,10))
        screen.blit(self.play,self.playCoords)
        screen.blit(self.info,self.infoCoords)
        screen.blit(self.scores,self.scoresCoords)
        screen.blit(self.scoreText,(410,60))
        screen.blit(self.exit,self.exitCoords)
