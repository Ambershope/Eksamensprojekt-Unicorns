import pygame
import random
import AiOponent
import BrikLogik
import GameObjects
import Database
import Networking
import Initialization
import Visuals
from Constants import *


Networking.NetConnecter
class Inputs:
    def __init__(self):
        self.quit = False
        self.mousePosition = [0,0]
        self.mouseLeftButtonDown = False
        self.overlayOpen = False
        #only active for a single frame
        self.closeOverlay = False
        self.mouseLeftButtonClick = False
        self.DEVTOOLdisplayGrid = False
        self.frameCounter = 0

    def update(self):
        self.frameCounter += 1
        self.mouseLeftButtonClick=False
        self.mousePosition=pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit=True

                # If the event type from Pygame says that a mouse button has been pressed,
                # and that event is that the left button has been presed while is isn't already pressed, then we set it to be pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pressed()
                if self.mouseLeftButtonDown == False and mouse[0] == True:
                    self.mouseLeftButtonDown = True
                    self.mouseLeftButtonClick = True
                
                # If Pygame event is that a button has been lifted, and its the left mouse, then we set left mouse down = false
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse=pygame.mouse.get_pressed()
                if mouse[0] == False:
                    self.mouseLeftButtonDown = False
            
            #detects the event as a key press
            elif event.type == pygame.KEYDOWN:
                #if the g key is pressed down
                if event.key == pygame.K_g:
                    self.DEVTOOLdisplayGrid = not self.DEVTOOLdisplayGrid

                elif event.key == pygame.K_ESCAPE and screenSelector != "start" and screenSelector != "main menu":
                    self.overlayOpen = not self.overlayOpen

        if self.closeOverlay:
            self.closeOverlay, self.overlayOpen = False, False
            




def main():
    #main program loop
    #Updates the input and calls either game() or startscreen() every frame
    while True:
        Input.update()

        if screenSelector != "start" and screenSelector != "main menu":
            if overlay() == "close game":
                return "close game"
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

        #draws the overlay on most screens
        if screenSelector != "start" and screenSelector != "main menu":
            Visuals.overlayDraw(Input, screen, Grid)

        #draws the underlying visual grid
        if Input.DEVTOOLdisplayGrid:
            Visuals.DEVTOOLdrawGrid(screen, Grid)
        
        Visuals.border(screen, Grid)
        
        clock.tick(FPS)
        pygame.display.update()

def game():
    '''
    Core game logic, called every frame while in game
    \nAlso calls drawGame()
    '''
    gameState
    

    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            global screenSelector
            screenSelector ="main menu"

    Visuals.drawGame(Input, screen, Grid, gameState)
    

def startScreen():
    '''
    Stuff for while on the start screen should
    \nhappen within this function, including drawing it
    '''
    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            global screenSelector
            screenSelector ="main menu"

    Visuals.drawStartScreen(screen)
   


def mainMenu():
    '''
    Stuff for while on the main menu should
    \nhappen within this function, including drawing it
    '''
    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            global screenSelector
            screenSelector = "gamemode"

    Visuals.mainMenuDraw(Input, screen, Grid)
    


def gamemodeSelect():
    '''
    Stuff for while on the gamemode selection screen should
    \nhappen within this function, including drawing it
    '''
    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            global screenSelector
            screenSelector ="game"
    Visuals.gamemodeScreenDraw(Input, screen, Grid)

def overlay():
    '''
    The overlay on most screens
    '''
    if Input.overlayOpen:
        if Input.mouseLeftButtonClick and not testColision(Grid.getGrid(Input.mousePosition),(10,4),(22,14)):
            Input.closeOverlay = True
        
        if Input.mouseLeftButtonClick and testColision(Grid.getGrid(Input.mousePosition),(12,12),(20,13)):
            return "close game"
    else:
        if Input.mouseLeftButtonClick and testColision(Grid.getGrid(Input.mousePosition),(31,0),(32,1)):
            Input.overlayOpen = True


def testColision(position, cornerA, cornerB):
    '''
    Test if a position is within a rectangle
    '''
    #test if in range of x
    if position[0]>=min(cornerA[0], cornerB[0]) and position[0]<=max(cornerA[0], cornerB[0]):

        #test if in range of y
        if position[1]>=min(cornerA[1], cornerB[1]) and position[1]<=max(cornerA[1], cornerB[1]):
            return True
    return False


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
#Initialization.innitialise()


screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.SRCALPHA)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
screenSelector="start"
Input=Inputs()
Grid=Visuals.Grid(screen)

#midlertidig gameState, ændres inden et spil startes
gameState=BrikLogik.GameState(GameObjects.Field(2),GameObjects.Pile("Default"))


main()
pygame.quit()