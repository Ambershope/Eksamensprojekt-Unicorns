import pygame
import random
import AiOponent
import BrikLogik
import GameObjects
import Database
import Networking
import Initialization
from Visuals import *
from Constants import *


Networking.NetConnecter
class Inputs:
    def __init__(self):
        self.quit=False
        self.mousePosition=[-1,-1]
        self.mouseLeftButtonDown=False

        #only active for a single frame
        self.mouseLeftButtonClick=False
        
        self.frameCounter = 0

    def update(self):
        self.frameCounter += 1
        self.mouseLeftButtonClick=False
        self.mousePosition=pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit=True

                # If the event type from Pygame says that a button has been pressed,
                # and that event is that the left button has been presed while is isnt already pressed, then we set it to be pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pressed()
                if self.mouseLeftButtonDown == False and mouse[0] == True:
                    self.mouseLeftButtonDown = True
                    self.mouseLeftButtonClick = True
                
                # If Pygame event is that a button has been liften, and its the left mouse, then we set left mouse down = false
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse=pygame.mouse.get_pressed()
                if mouse[0] == False:
                    self.mouseLeftButtonDown = False

        

def main():
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
        elif screenSelector == "main menu":
            mainMenu()
        elif screenSelector == "gamemode":
            gamemodeSelect()
        else:
            #this should NOT happen
            print("Error: screenSelector variable =",screenSelector)
        if screenSelector != "start" and screenSelector != "main menu":
            if overlay() == "close game":
                return "close game"
        pygame.display.update()
        clock.tick(FPS)

def game():
    '''
Core game logic, called every frame while in game
\nAlso calls drawGame()
    '''
    if Input.mouseLeftButtonClick == True:
        global screenSelector
        screenSelector ="main menu"
    drawGame(Input, screen)


def startScreen():
    '''
Stuff for while on the start screen should
\nhappen within this function, including drawing it
    '''
    if Input.mouseLeftButtonClick == True:
        global screenSelector
        screenSelector ="main menu"
    drawStartScreen(screen)
   


def mainMenu():
    '''
Stuff for while on the main menu should
\nhappen within this function, including drawing it
    '''
    if Input.mouseLeftButtonClick == True:
        global screenSelector
        screenSelector = "gamemode"
    mainMenuDraw(Input, screen)
    


def gamemodeSelect():
    '''Stuff for while on the gamemode selection screen should
\nhappen within this function, including drawing it
    '''
    if Input.mouseLeftButtonClick == True:
        global screenSelector
        screenSelector ="game"
    gamemodeScreenDraw(Input, screen)

def overlay():
    '''The overlay on most screens'''
    
    if Input.mouseLeftButtonClick and Input.mousePosition[0]<50 and Input.mousePosition[1]<50:
        return "close game"
    
    overlayDraw(Input, screen)




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
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
frameCounter=1
screenSelector="start"
Input=Inputs()
tileSizeX=screen.get_width()/GRID_LENGTH_X
tileSizeY=screen.get_height()/GRID_LENGTH_Y
print(tileSizeX,tileSizeY)
main()
pygame.quit()





"test"