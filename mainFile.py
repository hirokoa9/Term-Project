# pygame starting code from the pygame optional lecture
# https://github.com/LBPeraza/Pygame-Asteroids/blob/master/pygamegame.py

# all images and sounds except the beam are taken from the internet

# building.png http://sulmin.info/black-and-white-apartment-building-clip-art/
#    apartment-building-clipart-black-and-white-complex-china-cps-1/
# exlosion.ogg http://taira-komori.jpn.org/arms01.html
# explosion.png http://clipart-library.com/clipart/285954.htm
# gameBGM.ogg http://www.music-note.jp/bgm/sf.html
# gameclear.wav https://www.senses-circuit.com/material/se_game.html
# gameover.wav https://www.youtube.com/watch?v=Dz2Fk3SB-kI
# Heart.png http://www.hmcoloringpages.com/heart-silhouettes/
#    heart-silhouette-998/
# house.png https://karlaa-gonzaleez.deviantart.com/art/Casita-PNG-426992196
# missile.png https://openclipart.org/detail/254310/bomb-silhouette
# score.wav http://taira-komori.jpn.org/game01.html
# stick_figure.png https://thenounproject.com/term/stick-figure/203593/
# ufo.png https://pl.freepik.com/darmowe-ikony/statek-kosmiczny_727910.htm
# ufo.wav http://taira-komori.jpn.org/sf01.html
# flag.png https://commons.wikimedia.org/wiki/File:Emojione_BW_1F3F4.svg

import pygame
import random

from startScreen import Start
from howTo import Instructions
from gamePlay import Game
from gameOver import GameOver
from gameClear import GameClear
from scores import Scores

# run this file to play game

class Main(object):
    
# returns a list of past scores in order to generate score page and high score
    def getNumList(self,list):
        new=[]
        for i in range(len(list)):
            num=int(list[i][:-1])
            new.append(num)
        return new

    def __init__(self, width=600, height=400, fps=50, title="Planet Invader"):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()
        self.highScore=0
        self.score=0
        self.viewScores=Scores(self.highScore)
        self.scoreList=[]
        self.scoreList=self.viewScores.getScores('scores.txt')
        self.scoreList=self.getNumList(self.scoreList)
        self.highScore=max(self.scoreList)
        self.viewScores.drawList()
        self.intro=Start(self.highScore)
        self.tutorial=Instructions()
        self.gamePlay=Game(self.highScore)
        self.over=GameOver(self.highScore,self.score)
        self.clear=GameClear(self.highScore,self.score)
        self.start=True
        self.play=False
        self.howTo=False
        self.isOver=False
        self.congrats=False
        self.scores=False
        self._keys = dict()
        pygame.mixer.pre_init(44100,16,5,4096)
        pygame.mixer.init()

    def timerFired(self, dt):
        self.gamePlay.timerFired(dt)

# reset values after each mode change
    def resetTrans(self):
        self.intro.enterPlay=False
        self.intro.enterHowTo=False
        self.intro.enterScores=False
        self.tutorial.enterStart=False
        self.tutorial.pageOne=True
        self.viewScores.backMenu=False
        self.viewScores.drawList()
        self.gamePlay.gameOver=False
        self.gamePlay.gameClear=False
        self.gamePlay.pause=False
        self.gamePlay.player.x=260
        self.gamePlay.player.y=160
        self.gamePlay.gauge=0
        self.gamePlay.score=0
        self.gamePlay.time=0
        self.gamePlay.missileList.empty()
        self.gamePlay.humans.empty()
        self.gamePlay.houses.empty()
        self.gamePlay.buildings.empty()
        self.gamePlay.player.__init__(3,260,160)
        self.gamePlay.player.update(0,0)
        self.gamePlay.beam.__init__(230,240)
        self.gamePlay.beam.update(0,0)
        self.gamePlay.player.livesLeft=3
        self.over.back=False
        self.clear.back=False

# run all of the modes using booleans and while loops
    def run(self):
        clock = pygame.time.Clock()
        # screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # call game-specific initialization
        playing = True
        while playing:
            self.screen.fill(self.bgColor)
            while self.start:
                self.intro.getEvent()
                if self.intro.enterPlay:
                    self.start=False
                    self.play=True
                elif self.intro.enterHowTo:
                    self.start=False
                    self.howTo=True
                elif self.intro.exitGame:
                    playing=False
                    self.start=False
                elif self.intro.enterScores:
                    self.start=False
                    self.scores=True
                self.intro.redrawAll(self.screen)
                pygame.display.flip()
            while self.howTo:
                if self.tutorial.enterStart:
                    self.howTo=False
                    self.start=True
                self.tutorial.getEvent()
                self.tutorial.redrawAll(self.screen)
                pygame.display.flip()
            while self.scores:
                if self.viewScores.backMenu:
                    self.scores=False
                    self.start=True
                self.viewScores.getEvent()
                self.viewScores.redrawAll(self.screen)
                pygame.display.flip()
            while self.play:
                time = clock.tick(self.fps)
                self.timerFired(time)
                if not pygame.mixer.music.get_busy():
                    self.gamePlay.playMusic()
                if self.gamePlay.gameOver:
                    pygame.mixer.music.stop()
                    if self.gamePlay.score>self.highScore:
                        self.highScore=self.gamePlay.score
                    self.intro=Start(self.highScore)
                    self.viewScores.drawList()
                    if self.gamePlay.score>self.viewScores.scoreList[-9]:
                        self.viewScores.writeFile('scores.txt',"%d\n" \
                            % self.gamePlay.score)
                    self.play=False
                    self.isOver=True
                if self.gamePlay.gameClear:
                    pygame.mixer.music.stop()
                    if self.gamePlay.score>self.highScore:
                        self.highScore=self.gamePlay.score
                    self.intro=Start(self.highScore)
                    self.viewScores.drawList()
                    if self.gamePlay.score>self.viewScores.scoreList[-9]:
                        self.viewScores.writeFile('scores.txt',"%d\n" \
                            % self.gamePlay.score)
                    self.viewScores.writeFile('scores.txt',"%d\n" \
                        % self.gamePlay.score)
                    self.play=False
                    self.congrats=True
                self.gamePlay.getEvent()
                self.gamePlay.keys()
                self.gamePlay.redrawAll(self.screen)
                pygame.display.flip()
            while self.isOver:
                self.gamePlay.beamSound.stop()
                if self.over.back:
                    self.isOver=False
                    self.start=True
                self.over.getEvent()
                self.over.redrawAll(self.screen)
                pygame.display.flip()
            while self.congrats:
                self.gamePlay.beamSound.stop()
                if self.clear.back:
                    self.congrats=False
                    self.start=True
                self.clear.getEvent()
                self.clear.redrawAll(self.screen)
                pygame.display.flip()
            self.resetTrans()
        pygame.quit()


def main():
    game = Main()
    game.run()

if __name__ == '__main__':
    main()