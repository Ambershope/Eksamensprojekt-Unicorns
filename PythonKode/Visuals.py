import pygame
import Database
from Constants import *
from BrikLogik import GameState, Piece
import Knapper
class Grid:
    '''
    defines and calculates the size and location of the grid on a screen
    '''
    def __init__(self, screen):
        self.GRID_LENGTH_X=GRID_LENGTH_X
        self.GRID_LENGTH_Y=GRID_LENGTH_Y
        gridSizeX=screen.get_width()/GRID_LENGTH_X
        gridSizeY=screen.get_height()/GRID_LENGTH_Y
        self.gridSize=min(gridSizeX, gridSizeY)
        self.startX, self.startY = 0,0 

        if gridSizeX > gridSizeY:
            self.startX = (screen.get_width()-(self.gridSize*self.GRID_LENGTH_X))//2

        elif gridSizeY > gridSizeX:
            self.startY = ( screen.get_height()-(self.gridSize*self.GRID_LENGTH_Y))//2


    
    def getReal(self, gridCord=(0,0)):
        '''
        Turns a grid cordinate (0,0) into a real screen cordinate \nuses a tuple/list as input
        '''
        return ((gridCord[0] * self.gridSize + self.startX , gridCord[1] * self.gridSize + self.startY))
    
    def getGrid(self, realCord=(0,0)):
        return ((realCord[0]-self.startX)/self.gridSize,(realCord[1]-self.startY)/self.gridSize)
    
    def getRealLen(self, gridLength: int | float | tuple | list) -> int | float | list:
        
        if type(gridLength) == list or type(gridLength) == tuple:
            returnList=[]
            for i in gridLength:
                returnList.append(i*self.gridSize)
            return returnList
        
        else:
            return gridLength*self.gridSize
        
    def getGridLen(self, realLength: int | float | tuple | list) -> int | float | list:
        
        if type(realLength) == list or type(realLength) == tuple:
            returnList=[]
            for i in realLength:
                returnList.append(i/self.gridSize)
            return returnList
        
        else:
            return realLength/self.gridSize

class LoadedVariabels:
    '''
    A class for loading pictures into the game.
    \n This allows us to optimize loading, so that we don't load every picture -
    \nevery frame or store every picture in memory
    '''
    def __init__(self):
        '''This class doesn't need anything to be intizialised'''
        self.currentScreenLoaded = "none"
        pass
    def loadStartScreen(self, grid : Grid):
        image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","PiceTest1", ".png"))
        self.backgroundImg = pygame.transform.scale(image, grid.getRealLen((GRID_LENGTH_X,GRID_LENGTH_Y)))
        self.currentScreenLoaded = "start"

    def loadGameScreen(self, grid : Grid, gameState : GameState):
        tile0ImgUnscaled=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt", "TileNotPlaceble", ".png"))
        self.tile0Img=pygame.transform.scale( tile0ImgUnscaled, grid.getRealLen((gameState.tileSize,gameState.tileSize)))

        tile1ImgUnscaled=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt", "TilePlaceble", ".png"))
        self.tile1Img=pygame.transform.scale( tile1ImgUnscaled, grid.getRealLen((gameState.tileSize,gameState.tileSize)))
        self.currentScreenLoaded = "game"

    def loadGamemodeScreen(self, grid: Grid):
        self.networksBackgroundText = "Hello World!"
        self.networksBackgroundSize = grid.getRealLen((10.667, 14.4))
        self.networksBackgroundPos = grid.getReal((20, 1.8))
        self.networksBackground = pygame.transform.scale(pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","OpenNetworksBackground", ".png")), self.networksBackgroundSize)
        self.hostButtonSize = grid.getRealLen((10, 2.857))
        self.hostButtonPos = grid.getReal((2.05, 1.8))
        self.hostButton = pygame.transform.scale(pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","Host Button", ".png")), self.hostButtonSize)
        self.titleFont = pygame.font.SysFont("corbel.ttf", int(grid.getRealLen(2)))
        self.nameFont = pygame.font.SysFont("corbel.ttf", int(grid.getRealLen(1)))
        self.portFont = pygame.font.SysFont("corbel.ttf", int(grid.getRealLen(0.5)))
        self.fontColor = (0, 0, 0)

'''We create a loader that can be called from other scripts to load different classes'''
Loader = LoadedVariabels()

def mainMenuDraw(Input, screen, grid):
    '''
Draws the start screen\n
    '''
    screen.fill(BACKGROUND_COLOR)
    titleFont = pygame.font.SysFont(TITLE_FONT, int(grid.getRealLen(2)))
    img = titleFont.render(GAME_NAME, True, "white")
    
    
    screen.blit(img, ((grid.getRealLen(32) - img.get_width())/2, grid.getReal((0,1.5))[1]))




def gamemodeScreenDraw(Input, screen: pygame.surface.Surface, grid: Grid, servers: list[tuple]) -> list[tuple]:
    '''
    Draws the select gamemode screen.\n
    '''
    frameCounter = Input.frameCounter # Animations - tick
    returnlist = [] # List to return
    # Display background (Layer 1):
    screen.fill((150, 194, 145))
    # Display layer 2:
    screen.blit(Loader.networksBackground, Loader.networksBackgroundPos)
    screen.blit(Loader.hostButton, Loader.hostButtonPos)
    returnlist.append((Loader.hostButtonPos, (Loader.hostButtonPos[0] + Loader.hostButtonSize[0], Loader.hostButtonPos[1] + Loader.hostButtonSize[1]), "bh"))
    #Display layer 3 (Tekst?):
    screen.blit(Loader.titleFont.render(Loader.networksBackgroundText, True, Loader.fontColor), (Loader.networksBackgroundPos[0] + (Loader.networksBackground.get_rect()[2] - Loader.titleFont.size(Loader.networksBackgroundText)[0]) / 2, Loader.networksBackgroundPos[1] + grid.getRealLen(0.25)))
    otherReturns = len(returnlist)
    for i in range(len(servers)):
        name = servers[i][1]
        porttext = str(servers[i][0][0] + " : " + str(servers[i][0][1]))
        returnlist.append((
            (Loader.networksBackgroundPos[0], Loader.networksBackgroundPos[1] + grid.getRealLen(0.25)  + Loader.titleFont.size(Loader.networksBackgroundText)[1] + i * (Loader.nameFont.size(name)[1] + (Loader.portFont.size(porttext)[1]) + grid.getRealLen(0.25))), 
            (Loader.networksBackgroundPos[0] + Loader.networksBackgroundSize[0], Loader.networksBackgroundPos[1] + grid.getRealLen(0.25) + i * (Loader.nameFont.size(name)[1] + (Loader.portFont.size(porttext)[1]) + grid.getRealLen(0.25)) + Loader.titleFont.size(Loader.networksBackgroundText)[1] + Loader.nameFont.size("1")[1] + Loader.portFont.size("2")[1]), 
            "bj", servers[i][0]))
        screen.blit(Loader.nameFont.render(name, True, Loader.fontColor), (Loader.networksBackgroundPos[0] + (Loader.networksBackground.get_rect()[2] - Loader.nameFont.size(name)[0]) / 2, returnlist[i + otherReturns][0][1]))
        screen.blit(Loader.portFont.render(porttext, True, Loader.fontColor), (Loader.networksBackgroundPos[0] + (Loader.networksBackground.get_rect()[2] - Loader.portFont.size(porttext)[0]) / 2, returnlist[i + otherReturns][1][1] - Loader.portFont.size("Potato")[1]))
    return returnlist



def overlayDraw(Input, screen, grid):
    '''draws the overlay'''
    #creates the bruger meny that opens the overlay

    image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","ExitButton", ".png"))
    scaledImage=pygame.transform.scale(image, (grid.getRealLen((1,1))))

    screen.blit(scaledImage, grid.getReal((31, 0)))

    


    if Input.overlayOpen:
        #creates a dark seethroug layer that covers the entire screen
        alfaSurface=pygame.Surface(grid.getRealLen((GRID_LENGTH_X,GRID_LENGTH_Y)))
        alfaSurface.set_alpha(128)
        alfaSurface.fill((0,0,0))
        screen.blit(alfaSurface, grid.getReal((0,0)))

        #creates the underlying box for the options full screen overlay
        pygame.draw.rect(screen, OPTIONS_BACKGROUND, (grid.getReal((10,4)),grid.getReal((GRID_LENGTH_X-20,GRID_LENGTH_Y-8))), border_radius=round(grid.gridSize*0.5))

        #creates the quit game button
        exitTextFont=pygame.font.SysFont(FONT, int(grid.gridSize*2))
        exitTextImage=exitTextFont.render("Exit?", True, "BLUE")
        exitImage=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","ExitButton", ".png"))
        scaledImage=pygame.transform.scale(exitImage, grid.getRealLen((8,1)))
        screen.blit(scaledImage, grid.getReal((12, 12)))
        screen.blit(exitTextImage, grid.getReal((14.5,8)))
        
    

def drawStartScreen(screen, grid):
    '''
Draws the start screen\n
    '''  
    #clears the screen
    screen.fill((0,0,0))
    
    #draws the startscreen art
    screen.blit(Loader.backgroundImg, grid.getReal((0, 0)))


    


def drawGame(Input, screen : pygame.surface, grid, gameState:GameState, hoveringPiece: Piece | int, hoveringHand : int):
    '''
Draws the game\n
    '''

    screen.fill(SUNSHINE)

    #draw the facy top infobar
    pygame.draw.rect(screen, PINK, (grid.getReal((0,0)),grid.getRealLen((32,1.1))))
    #draw field base
    pygame.draw.rect(screen, BACKGROUND_COLOR, (grid.getReal((7,0)),grid.getRealLen((18,18))))

    
    #draw field

    #for each location on the field, 
    for xField in range (gameState.field.fieldSize):
        xGrid=(xField*gameState.tileSize)+7+((xField+1)*GRID_BETWEEN_TILES)

        for yField in range (gameState.field.fieldSize):
            yGrid=(yField*gameState.tileSize)+((yField+1)*GRID_BETWEEN_TILES)

            currentTileValue=gameState.field.tileField[xField][yField]
            currentPieceValue=gameState.field.pieceField[xField][yField]

            #place the appropriate tile
            if currentTileValue==0:
                screen.blit(Loader.tile0Img, grid.getReal((xGrid, yGrid)))
            else:
                screen.blit(Loader.tile1Img, grid.getReal((xGrid, yGrid)))

            #Draw the appropiate piece
            if currentPieceValue != 0:
                currentPieceValue.drawMe(screen, grid.getReal((xGrid+0.25, yGrid+0.25)),grid.getRealLen(gameState.tileSize-0.5))
    #draw the hand
    handInfoSize = 5
    for i in range (len(gameState.hand)+1):
        drawYCorner = (handInfoSize*(i%3)) + (0.45*((i%3)+1)) + 1.1
        drawXCorner = 1 + ((i//3)*(18+7))
        if i < len(gameState.hand):
            currentPieceValue= gameState.hand[i]
            if currentPieceValue != 0:
                currentPieceValue.drawMe(screen, grid.getReal((drawXCorner, drawYCorner)), grid.getRealLen(handInfoSize), True)
            else:
                pygame.draw.rect(screen, MINT_GREEN, (grid.getReal((drawXCorner, drawYCorner)),grid.getRealLen((handInfoSize, handInfoSize))))
        else: # the end of the hand and the hover info tile
            pygame.draw.rect(screen, (CONTRAST1), (grid.getReal((drawXCorner, drawYCorner)),grid.getRealLen((handInfoSize,handInfoSize))))
            if hoveringPiece != 0:
                
                flavortext = hoveringPiece.flavorText
                flavortextList = flavortext.split()
                flavortextIteration = 0


                x, y = grid.getReal((drawXCorner, drawYCorner))
                xpos = x
                ypos = y
                sentenceWidth = 0

                squareLength = grid.getRealLen(5)
                flavorFont = pygame.font.SysFont(None,40)
                spaceWidth = flavorFont.size(" ")[0]

                for flavortextIteration in range (len(flavortextList)):
                    flavortextRender = flavorFont.render(flavortextList[flavortextIteration],True,"BLACK")
                    wordWidth = flavortextRender.get_width()
                    wordHeight= flavortextRender.get_height()

                    if sentenceWidth + wordWidth > squareLength:
                        xpos = x
                        sentenceWidth = 0
                        ypos += wordHeight
                    
                    screen.blit(flavortextRender, (xpos + sentenceWidth,ypos))
                    sentenceWidth += wordWidth + spaceWidth
                    flavortextIteration += 1
                

                '''
                Psudokode :))

                Get size of boks (getReal/getRealLen?)

                Lav en liste med ord fra flavorteksten (det kan man gøre ved at bruge flavortext.split)
                
                #hoveringPiece.drawMe(screen, grid.getReal((drawXCorner, drawYCorner)), grid.getRealLen(gameState.tileSize-1))
                '''
    
    pieceCountTextFont=pygame.font.SysFont(FONT, int(grid.gridSize*1.8))
    yoursImage=pieceCountTextFont.render(str(gameState.field.yourPieces), True, YOUR_COLOR)
    opponentsImage=pieceCountTextFont.render(str(gameState.field.opponentPieces), True, OPPONENT_COLOR)
    
    screen.blit(yoursImage, grid.getReal((3-grid.getGridLen(yoursImage.get_width()),0)))
    screen.blit(opponentsImage, grid.getReal((6.5-grid.getGridLen(opponentsImage.get_width()),0)))

            
    #draws the piece in hand at the center of the cursor position         
    if gameState.holdingPiece != 0:
        gameState.holdingPiece.drawMe(screen, (Input.mousePosition[0]-(grid.getRealLen(gameState.tileSize-0.5)//2),Input.mousePosition[1]-(grid.getRealLen(gameState.tileSize-0.5)//2)), grid.getRealLen(gameState.tileSize-0.5))


    '''changes the cursor'''
    #if the user is holding a piece in hand
    if Input.isHolding:

        holdingCursor= pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEALL)
        pygame.mouse.set_cursor(holdingCursor)

    elif gameState.turnCycleStep == 0 : #if its the users turn to select a piece
        #If they are hovering a piece in hand
        if hoveringHand != -1: pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        
        else: pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    #the cursor when it isn't the users turn
    else: pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))

    

    
  
        



    

def border(screen, grid):
    '''
    draws the border around the grid
    '''
    if grid.startY != 0:
        pygame.draw.rect(screen, BORDER_COLOR, ((0,0),grid.getReal((GRID_LENGTH_X,0))))
        pygame.draw.rect(screen, BORDER_COLOR, (grid.getReal((0,GRID_LENGTH_Y)),(screen.get_width(), screen.get_height())))
        
    if grid.startX !=0:
        pygame.draw.rect(screen, BORDER_COLOR, ((0,0),grid.getReal((0,GRID_LENGTH_Y))))
        pygame.draw.rect(screen, BORDER_COLOR, (grid.getReal((GRID_LENGTH_X,0)),(screen.get_width(), screen.get_height())))

def DEVTOOLdrawGrid(screen, grid):
    '''
draws the underlying visual grid for development use, toggel with g at the time of writing
    '''
    for y in range (GRID_LENGTH_Y+1):
        pygame.draw.line(screen, "black", grid.getReal((0,y)), grid.getReal((GRID_LENGTH_X,y)), 1)
    for x in range (GRID_LENGTH_X+1):
        pygame.draw.line(screen, "black", grid.getReal((x,0)), grid.getReal((x,GRID_LENGTH_Y)), 1)

if __name__ == "__main__":
    import main