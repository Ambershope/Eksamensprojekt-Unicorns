import pygame
import random
import AiOponent
import BrikLogik
import GameObjects
import Database
import Networking
from Constants import *



class Inputs:
    def __init__(self):
        self.quit=False
        self.mousePosition=[-1,-1]
        self.mouseLeftButtonDown=False

        #only active for a single frame
        self.mouseLeftButtonClick=False

    def update(self):
        self.mouseLeftButtonClick=False
        self.mousePosition=pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit=True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pressed()
                if self.mouseLeftButtonDown == False and mouse[0] == True:
                    self.mouseLeftButtonDown = True
                    self.mouseLeftButtonClick = True
                
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse=pygame.mouse.get_pressed()
                if mouse[0] == False:
                    self.mouseLeftButtonDown = False

        

def main():
    global frameCounter
    #main program loop
    #Updates the input and calls either game() or startscreen() every frame
    while True:
        Input.update()

        if Input.quit == True:
            return "close game"
        
        if screenSelector == "game":
            game()
        elif screenSelector == "start":
            startScreen()
        else:
            #this should NOT happen
            print("Error: screenSelector variable =",screenSelector)
        

        pygame.display.update()
        clock.tick(FPS)
        frameCounter += 1

def game():
    '''
Core game logic, called every frame while in game
\nAlso calls drawGame()
    '''
    if Input.mouseLeftButtonClick == True:
        global screenSelector
        screenSelector ="start"
    drawGame()

#visuals for the core game
def drawGame():
    global frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,brightness,0))


def startScreen():
    '''
Stuff for while on the start screen should
\nhappen within this function, including drawing it
    '''
    if Input.mouseLeftButtonClick == True:
        global screenSelector
        screenSelector ="game"
    drawStartScreen()

#visuals for the startscreen    
def drawStartScreen():
    global frameCounter
    brightness=abs(255-((frameCounter*3)%511))
    screen.fill((0,0,brightness))




def startGame():
    while True:
        #userInputs
        drawBrick()
        sendTurn()
        if checkWin(): 
            youWin()
            break
        opponentTurn()
        if checkWin(): 
            opponentWin()
            break


'''#Whats a brick?'''
def drawBrick():
    pass

def opponentTurn():
    idelWait()
    pass

def idelWait():
    pass

def checkWin():
    return False

def sendTurn():
    pass

def youWin():
    pass

def opponentWin():
    pass


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Unicorn Fight Club")
clock = pygame.time.Clock()
frameCounter=1
screenSelector="start"
Input=Inputs()

main()
pygame.quit()