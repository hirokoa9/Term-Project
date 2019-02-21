import pygame

# how to play mode
class Instructions(object):

# loads and configures images and texts    
    def __init__(self):
        self.HowTo=pygame.image.load('images/HowTo.png').convert_alpha()
        self.HowTo2=pygame.image.load('images/HowTo2.png').convert_alpha()
        self.miniFont=pygame.font.SysFont("Comic Sans MS", 25)
        self.next=self.miniFont.render("NEXT", False, (0, 0, 0))
        self.back=self.miniFont.render("BACK", False, (0, 0, 0))
        self.done=self.miniFont.render("DONE", False, (0, 0, 0))
        self.nextCoord=(525,377)
        self.backCoord=(29,372)
        self.doneCoord=(530,372)
        self.pageOne=True
        self.enterStart=False
        self._keys = dict()
 
# keeps track of mouse clicks on buttons
    def mousePressed(self, x, y):
        if self.pageOne:
            nextButton=self.next.get_rect()
            nextButton.move_ip(self.nextCoord)
            if nextButton.collidepoint(x,y):
                self.pageOne=False
        else:
            backButton=self.back.get_rect()
            backButton.move_ip(self.backCoord)
            if backButton.collidepoint(x,y):
                self.pageOne=True
            doneButton=self.done.get_rect()
            doneButton.move_ip(self.doneCoord)
            if doneButton.collidepoint(x,y):
                self.enterStart=True
                
# keeps track of keys pressed to navigate pages
    def keyPressed(self, keyCode, modifier):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.pageOne:
                self.pageOne=False
        if keys[pygame.K_LEFT]:
            if self.pageOne==False:
                self.pageOne=True
        if keys[pygame.K_RETURN]:
            if self.pageOne==False:
                self.enterStart=True

    def getEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos))
            elif event.type == pygame.KEYDOWN:
                self._keys[event.key] = True
                self.keyPressed(event.key, event.mod)

# draws images and text on screen
    def redrawAll(self, screen):
        if self.pageOne:
            screen.blit(self.HowTo,self.HowTo.get_rect())
            screen.blit(self.next,self.nextCoord)
        else:
            screen.blit(self.HowTo2,self.HowTo2.get_rect())
            screen.blit(self.back,self.backCoord)
            screen.blit(self.done,self.doneCoord)
        