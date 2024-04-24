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
        self.isHolding = False

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
        network.leaveServerLister()
    screenSelector = target
    # Code that runs, when you enter a screen:
    if screenSelector == "gamemode":
        Visuals.Loader.loadGamemodeScreen(Grid)
        network.serverLister()



def game():
    '''
    Core game logic, called every frame while in game
    \nAlso calls drawGame()
    '''


     #hovering detection
    gridMouse=Grid.getGrid(Input.mousePosition)
    hoveringHand = -1
    hoveringPiece = 0
    isHoveringField = False


    if gridMouse[0] <= 7 or gridMouse[0] >= 25: #hand left
        handTileGrid = 5
        for i in range (len(gameState.hand)):

            yGrid = (handTileGrid*(i%3)) + (0.45*((i%3)+1)) + 1.1
            xGrid = 1 + ((i//3)*(18+7))

            if gridMouse[0] >= xGrid and gridMouse[0] <= xGrid + handTileGrid:
                if gridMouse[1] >= yGrid and gridMouse[1] <= yGrid + handTileGrid:

                    currentPieceValue= gameState.hand[i]
                    if currentPieceValue != 0:
                        hoveringHand = i
                        hoveringPiece = currentPieceValue

    else: #center
        xField, yField = -1, -1
        for x in range (gameState.field.fieldSize):
            xGrid=(x*gameState.tileSize)+7+((x+1)*GRID_BETWEEN_TILES)
            if gridMouse[0] >= xGrid and gridMouse[0] <= xGrid + gameState.tileSize:
                xField = x
                break        

        for y in range (gameState.field.fieldSize):
            yGrid=(y*gameState.tileSize)+((y+1)*GRID_BETWEEN_TILES)
            if gridMouse[1] >= yGrid and gridMouse[1] <= yGrid + gameState.tileSize:
                yField = y
                break
        
        if xField != -1 and yField != -1:
            isHoveringField = True
            hoveringPiece=gameState.field.pieceField[xField][yField]

    '''since the game has many different things to do, 
    depending on were on a turn cycle the players are,
    it figures it out in this massive case'''

    match gameState.turnCycleStep:
        case 0: #you select piece (form hand)
            if not Input.overlayOpen and Input.mouseLeftButtonClick and hoveringHand != -1:
                Input.isHolding = True
                gameState.holdingPiece=hoveringPiece
                gameState.hand[hoveringHand] = 0
                gameState.newTurnStep()
            

        case  1: #you select tile (from field)
            hoveringPiece = gameState.holdingPiece

            #when held button is released
            if Input.mouseLeftButtonDown == False:
                Input.isHolding = False

                #test if it is possible to place the piece in the selectet tile
                if isHoveringField and gameState.field.isPlacable((xField,yField)):
                    gameState.placePiece((xField,yField))
                    gameState.newTurnStep()

                else: #if it isnt possible, go back a step to turnCycleStep 0
                    gameState.turnCycleStep = 0
                    for i in range (len(gameState.hand)):
                        if gameState.hand[i] == 0:
                            gameState.hand[i] = gameState.holdingPiece
                            gameState.holdingPiece = 0
                            break
                

        case  2: #send to opponent (send selection to opponent)
            network.sendTCPMessage("ET:" + str(gameState.newestPiece[0]) + ";" + str(gameState.newestPiece[1]) + ":" + str(gameState.field.pieceField[gameState.newestPiece[0]][gameState.newestPiece[1]].pieceId))
            gameState.newTurnStep()

        case  5: #draw back too 5 pieces (draw missing pieces at the end of turn)
            gameState.fillHand()
            gameState.newTurnStep()

        case 6: #wait for opponent
            pass
            

        case  4 | 8: #test if game is over (test win)
            
            if gameState.field.testGameOver() == False:
                gameState.newTurnStep()

            else:
                if gameState.field.yourPieces > gameState.field.opponentPieces:
                    #youWin
                    pass
                elif gameState.field.opponentPieces < gameState.field.yourPieces:
                    #opponentWins
                    pass
                else:
                    #no one wins
                    pass
                

        case -1: #(select fist player)
            # we gotta make it so the server randomly decides. for now you always start.
            # aka. bjørn plz fiks
            gameState.newTurnStep()

        case -2: #draw start hands of 5 pieces
            gameState.fillHand()
            gameState.newTurnStep()

        case _ : #gameState.turnCycleStep == 3 or 7 #place pieces on field etb A or B
            attack()
            gameState.newTurnStep()
            

    Visuals.drawGame(Input, screen, Grid, gameState, hoveringPiece)

def attack():
    print ("attack from " + str(gameState.newestPiece))
    if gameState.newestPiece != (-1,-1):
        attackingPiece = gameState.field.pieceField[gameState.newestPiece[0]][gameState.newestPiece[1]]
        distance = attackingPiece.persuasionRange #normally 1 sometimes 2
        directionCords =(0*distance,-1*distance)
        for direction in range(4):
            print(direction)
            print(directionCords)
            if directionCords[0]+gameState.newestPiece[0] < 0 or directionCords[0]+gameState.newestPiece[0] >= gameState.field.fieldSize or directionCords[1]+gameState.newestPiece[1]< 0 or directionCords[1]+gameState.newestPiece[1] >= gameState.field.fieldSize:
                print("continue")
                directionCords = BrikLogik.tvearVektor(directionCords)
                continue

            targetPieceValue = gameState.field.pieceField[gameState.newestPiece[0]+directionCords[0]][gameState.newestPiece[1]+directionCords[1]]
            if targetPieceValue != 0:
                if targetPieceValue.isYours == False:
                    if targetPieceValue.persuasion[direction-2] <= attackingPiece.persuasion[direction]:
                        print("hit me baby ine more time")
                        gameState.field.pieceField[gameState.newestPiece[0]+directionCords[0]][gameState.newestPiece[1]+directionCords[1]].isYours = attackingPiece.isYours

            directionCords = BrikLogik.tvearVektor(directionCords)
       
     
 
   
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
    # if not Input.overlayOpen:
    #     if Input.mouseLeftButtonClick == True:
    #         switchScreen("game")
    interatives = Visuals.gamemodeScreenDraw(Input, screen, Grid, network.openServers)
    for tmp in interatives:
        if tmp[2].startswith("b"):
            if tmp[2].find("j")+1:
                if Knapperne.knap(Input, tmp[0], tmp[1]):
                    print(tmp[3])
                    if not(network.connectTCPPort(tmp[3])):
                        switchScreen("game")
                        print("Joined Game on port: {}".format(tmp[3]))
            elif tmp[2].find("h")+1:
                if Knapperne.knap(Input, tmp[0], tmp[1]):
                    print("Hosting a GAME!!!")
                    network.leaveServerLister()
                    network.broadcastServer()

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



def networkingReader(message: str):
    message = message.replace(" ", "")
    message = message.split(":")
    if message[0] == "ET":
        receivedPieceId = message[2]
        tmp = message[1].split(";")
        receivedPieceCords = (int(tmp[0]), int(tmp[1]))
        gameState.holdingPiece = BrikLogik.Piece(receivedPieceId, False)
        gameState.placePiece(receivedPieceCords)
        gameState.newTurnStep()
    
    print(message)

def opponentJoinedGame():
    switchScreen("game")
    print("An opponent has joined the game at ", network.client)

pygame.init()
#Initialization.innitialise()


screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.SRCALPHA)
network = Networking.NetConnecter()
network.processFunk = networkingReader
network.foundOpponentFunk = opponentJoinedGame
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
screenSelector="start"
Input=Inputs()
Grid=Visuals.Grid(screen)
Knapperne = KnappeDetection()

#midlertidig gameState, ændres inden et spil startes
gameState=BrikLogik.GameState(GameObjects.Field(1),GameObjects.Pile("Default"))

with open(Database.pathToGameDataFile("Databases", "Settings"), "r") as settingsFile:
    while True:
        setting = settingsFile.readline()
        if setting == "#!#\n": break
        elif setting.startswith("Name"): network.serverName = setting.split(":")[1].strip()
    print("Settings Loaded!")

main()
pygame.quit()