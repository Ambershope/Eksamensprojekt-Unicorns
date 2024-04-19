import pygame
import random
import AiOpponent
import BrikLogik
import GameObjects
import Database
import Networking
import Initialization
from Knapper import KnappeDetection
import Visuals
from Constants import *


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

def switchScreen(target: str) -> None:
    global screenSelector
    # Code that runs, when you leave a screen:
    if screenSelector == "gamemode":
        network.serverLister()
    screenSelector = target
    # Code that runs, when you enter a screen:
    if screenSelector == "gamemode":
        network.leaveServerLister()



def game():
    '''
    Core game logic, called every frame while in game
    \nAlso calls drawGame()
    '''

    '''since the game has many different things to do, 
    depending on were on a turncycle the players are,
    it figures it out in this massive if-elif statement'''
    
    if gameState.turnCycleStep == 0: #you select piece (form hand)
        pass

    elif gameState.turnCycleStep == 1: #you select tile (from field)
        pass

    elif gameState.turnCycleStep == 2: #send to opponent (send selection to opponent)
        #bjørn plz fiks
        gameState.newTurnStep()

    elif gameState.turnCycleStep == 5: #draw back too 5 pieces (draw missing pieces at the end of turn)
        gameState.fillHand()
        gameState.newTurnStep()

    elif gameState.turnCycleStep == 6: #wait for opponent
        #bjørn plz fiks
        pass

    elif gameState.turnCycleStep == 4 or gameState.turnCycleStep == 8: #test if game is over (test win)
        pass

    elif gameState.turnCycleStep == -1: #(select fist player)
        pass

    elif gameState.turnCycleStep == -2: #draw start hands of 5 pieces
        gameState.fillHand()
        gameState.newTurnStep()

    else: #gameState.turnCycleStep == 3 or 7 #place pieces on field etb A or B
        pass

    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            switchScreen("main menu")

    Visuals.drawGame(Input, screen, Grid, gameState)
    

def startScreen():
    '''
    Stuff for while on the start screen should
    \nhappen within this function, including drawing it
    '''
    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            switchScreen("main menu")

    Visuals.drawStartScreen(screen, Grid)
   


def mainMenu():
    '''
    Stuff for while on the main menu should
    \nhappen within this function, including drawing it
    '''
    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            switchScreen("gamemode")
    

    Visuals.mainMenuDraw(Input, screen, Grid)
    


def gamemodeSelect(): # Bjørn arbejder på den lige nu
    '''
    Stuff for while on the gamemode selection screen should
    \nhappen within this function, including drawing it
    '''
    if not Input.overlayOpen:
        if Input.mouseLeftButtonClick == True:
            switchScreen("game")
    Visuals.gamemodeScreenDraw(Input, screen, Grid, network.openServers)

def overlay():
    '''
    The overlay on most screens
    '''
    if Input.overlayOpen:
        
        if Knapperne.antiKnap(Input,Grid.getReal((10,4)),Grid.getReal((22,14))):
            Input.closeOverlay = True
        
        if Knapperne.knap(Input,Grid.getReal((12,12)),Grid.getReal((20,13))):
            return "close game"
    else:
        if Knapperne.knap(Input,Grid.getReal((31,0)),Grid.getReal((32,1))):
            Input.overlayOpen = True 


def testColision(position: tuple, cornerA: tuple, cornerB: tuple) -> bool:
    '''
    Test if a position is within a rectangle
    '''
    #test if in range of x
    if position[0]>=min(cornerA[0], cornerB[0]) and position[0]<=max(cornerA[0], cornerB[0]):

        #test if in range of y
        if position[1]>=min(cornerA[1], cornerB[1]) and position[1]<=max(cornerA[1], cornerB[1]):
            return True
    return False


pygame.init()
#Initialization.innitialise()


screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.SRCALPHA)
network = Networking.NetConnecter()
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
screenSelector="start"
Input=Inputs()
Grid=Visuals.Grid(screen)
Knapperne = KnappeDetection()

#midlertidig gameState, ændres inden et spil startes
gameState=BrikLogik.GameState(GameObjects.Field(2),GameObjects.Pile("Default"))

fluttersej = BrikLogik.Piece(gameState.playerPile.drawPiece())
gameState = fluttersej.placeOnField(gameState, (2,4))


main()
pygame.quit()