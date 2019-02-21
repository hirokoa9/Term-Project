import pygame

# game over mode
class GameOver(object):
    
# loads and configures images and texts
    def __init__(self,score,highScore):
        self.back=False
        self.score=score
        self.highScore=highScore
        self.font=pygame.font.SysFont("Comic Sans MS", 120)
        self.text=self.font.render("GAME OVER",False,(0,0,0))
        self.minifont=pygame.font.SysFont("Comic Sans MS", 30)
        self.returnText=self.minifont.render("Return to Menu",False,(0,0,0))
        self.returnCoords=(390,200)
        self.explode=pygame.image.load('images/explosion.png').convert_alpha()
        self.explode=pygame.transform.scale(self.explode,(80,80))
        self._keys = dict()

# keeps track of mouse clicks on buttons
    def mousePressed(self, x, y):
        backButton=self.returnText.get_rect()
        backButton.move_ip(self.returnCoords)
        if backButton.collidepoint(x,y):
            self.back=True

    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos))

# draws text on screen
    def redrawAll(self, screen):
        screen.blit(self.text,(50,120))
        screen.blit(self.returnText,self.returnCoords)
