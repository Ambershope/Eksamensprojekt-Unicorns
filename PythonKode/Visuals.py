import pygame
import Database
from Constants import *

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
        returnList=[]
        if type(gridLength) == list or type(gridLength) == tuple:
            for i in gridLength:
                returnList.append(i*self.gridSize)
            return returnList
        else:
            return gridLength*self.gridSize
    

class LoadedVariabels:
    '''
    A class for loading pictures into the game.
    \n This allows us to optimize loading, so that we don't load every picture -
    \nevery frame or store every picture in memory
    '''
    def __init__(self):
        '''This class doesn't need anything to be intizialised'''
        pass

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

'''We create a loader that can be called from other scirptis to load difrent classes'''
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
        image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","ExitButton", ".png"))
        scaledImage=pygame.transform.scale(image, grid.getRealLen((8,1)))
        screen.blit(scaledImage, grid.getReal((12, 12)))
    

def drawStartScreen(screen, grid):
    '''
Draws the start screen\n
    '''

    #clears the screen
    screen.fill((0,0,0))
    
    #creates the startscreen art
    image=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt","PiceTest1", ".png"))
    scaledImage=pygame.transform.scale(image, grid.getRealLen((GRID_LENGTH_X,GRID_LENGTH_Y)))
    screen.blit(scaledImage, grid.getReal((0, 0)))
    


def drawGame(Input, screen, grid, gameState):
    '''
Draws the game\n
    '''
    screen.fill(SUNSHINE)

    #draw the facy top infobar
    pygame.draw.rect(screen, PINK, (grid.getReal((0,0)),grid.getRealLen((32,1.1))))
    #draw field base
    pygame.draw.rect(screen, BACKGROUND_COLOR, (grid.getReal((7,0)),grid.getRealLen((18,18))))

    
    #draw field
    #load in the different tiles 
    tile0ImgUnscaled=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt", "TileNotPlaceble", ".png"))
    tile0Img=pygame.transform.scale( tile0ImgUnscaled, grid.getRealLen((gameState.tileSize,gameState.tileSize)))

    tile1ImgUnscaled=pygame.image.load(Database.pathToGameDataFile("Visuals\DevArt", "TilePlaceble", ".png"))
    tile1Img=pygame.transform.scale( tile1ImgUnscaled, grid.getRealLen((gameState.tileSize,gameState.tileSize)))

    #for each location on the field, 
    for xField in range (gameState.field.fieldSize):
        xGrid=(xField*gameState.tileSize)+7+((xField+1)*GRID_BETWEEN_TILES)

        for yField in range (gameState.field.fieldSize):
            yGrid=(yField*gameState.tileSize)+((yField+1)*GRID_BETWEEN_TILES)

            currentTileValue=gameState.field.tileField[xField][yField]
            currentPieceValue=gameState.field.pieceField[xField][yField]

            #place the appropriate tile
            if currentTileValue==0:
                screen.blit(tile0Img, grid.getReal((xGrid, yGrid)))
            else:
                screen.blit(tile1Img, grid.getReal((xGrid, yGrid)))

            #place the appropiate piece
            if currentPieceValue != 0:
                currentPieceValue.drawMe(screen, grid.getReal((xGrid+0.25, yGrid+0.25)),grid.getRealLen(gameState.tileSize-0.5))


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