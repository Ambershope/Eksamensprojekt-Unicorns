class Piece:
    def __init__ (self, pieceName):
        self.pieceName=pieceName
        #self.Attack = [N, S, E, W] ?
        #self.artwork = 
        #self.effectFunction = 
        self.explainingText = "lol no text"

class GameState:
    def __init__(self, field_, playerPile_):
        self.field=field_
        self.playerPile=playerPile_
        self.turnCycleStep=0
        self.turnCycleTable=["Select First Player", "Draw Start Hands", 
                             "You Select Piece", "You Select Tile", "Send To Opponent", "Piece ETB (A)", "Test Win(A)", 
                             "Wait For Opponent", "Piece ETB (B)", "Test Win (B)" ]
