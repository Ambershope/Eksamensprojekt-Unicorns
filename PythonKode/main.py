import pygame
import AiOponent
import BrikLogik
import GameObjects
import Database
import Networking
from Constants import FPS

pygame.init()


screensize = (800, 1200)
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()

def main():
    startGame()


def startGame():
    while True:
        userInput()
        drawBrick()
        sendTurn()
        if checkWin(): 
            youWin()
            break
        opponentTurn()
        if checkWin(): 
            opponentWin()
            break

        drawStep()

def userInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pass

def drawBrick():
    pass

def opponentTurn():
    idelWait()
    pass

def idelWait():
    pass

def checkWin():
    return True

def sendTurn():
    pass

def drawStep():
    pygame.display.update()
    clock.tick(FPS)

def youWin():
    pass

def opponentWin():
    pass

main()
pygame.quit()