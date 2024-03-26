import Database

class Piece:
    def __init__ (self, pieceId_, isYours_=True):
        cardData = Database.databaseCardFinder(pieceId_)[0]
        self.pieceName= cardData[1]
        print(self.pieceName)
        self.pieceName = pieceId_
        self.isYours=isYours_
        self.persuasion= [cardData[3], cardData[4], cardData[5], cardData[6]]
        self.persuasion= [0, 0, 0, 0]
        self.artworkPath = ""
        # self.artwork = 
        self.effectFunctionId = 0
        self.explainingText = "lol no text"

class GameState:
    def __init__(self, field_, playerPile_):
        self.field=field_
        self.playerPile=playerPile_
        self.turnCycleStep=-2
        self.startCycle=["Draw Start Hands", "Select First Player"]
        self.turnCycleTable=["You Select Piece", "You Select Tile", "Send To Opponent", "Piece ETB (A)", "Test Win(A)", "Draw Card", 
                             "Wait For Opponent", "Piece ETB (B)", "Test Win (B)"]

Piece(1)