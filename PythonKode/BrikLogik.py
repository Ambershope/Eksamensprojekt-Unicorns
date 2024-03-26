class Piece:
    def __init__ (self, pieceName, isYours_=True):
        self.pieceName=pieceName
        self.id = 0
        self.isYours=isYours_
        self.persuasion= [0, 0, 0, 0]
        self.will = self.persuasion
        # self.artworkPath =
        # self.artwork = 
        # self.effectFunction = 
        self.explainingText = "lol no text"

class GameState:
    def __init__(self, field_, playerPile_):
        self.field=field_
        self.playerPile=playerPile_
        self.turnCycleStep=-2
        self.startCycle=["Draw Start Hands", "Select First Player"]
        self.turnCycleTable=["You Select Piece", "You Select Tile", "Send To Opponent", "Piece ETB (A)", "Test Win(A)", "Draw Card", 
                             "Wait For Opponent", "Piece ETB (B)", "Test Win (B)"]