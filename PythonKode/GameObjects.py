import random
from Database import pathToGameDataFile
from Constants import MAX_DUPES_IN_PILE

class Field:
    def __init__ (self, fieldId=0):
        self.fieldId=fieldId
        self.tileField=self.getStartField()
        self.pieceField=self.getFullField()

    def __str__ (self):
        '''
        returnere en string med et flot formateret field
        '''
        tekst="\ntile layer\n"

        for y in range (self.fieldSize):
            for x in range (self.fieldSize):
                tekst += " " + str(self.tileField[x][y]) + " "
            tekst += "\n"
        tekst += "\npiece layer\n"
        for y in range (self.fieldSize):
            for x in range (self.fieldSize):
                tekst += " " + str(self.pieceField[x][y]) + " "
            tekst += "\n"

        return tekst
    
    def getFullField(self, value=0):
        '''
        creates a square field that is full of the specified value,\n
        and has a side length = self.fieldSize
        '''
        field=[]
        yField=[]

        for y in range (self.fieldSize):
            yField.append(value)

        for x in range (self.fieldSize):
            field.append(list(yField))

        return field

        
    def getStartField(self):
        #får field ind i fieldData
        file=open(pathToGameDataFile("Maps","Map"+str(self.fieldId)), 'r')
        fieldData=file.read().split("\n")
        file.close()

        #finder sidelængden på banen
        sizeX=len(fieldData[0])
        sizeY=len(fieldData)
        if sizeX == sizeY:
            self.fieldSize=sizeX
        else:
            print("Error: map not square. Entire map wont load")
            if sizeX > sizeY:
                self.fieldSize=sizeY
            else:
                self.fieldSize=sizeX

        #formaterer kortet og sørger for at lave en tabel med int's
        field=[]
        for x in range (self.fieldSize):
            yValues=[]
            for y in range (self.fieldSize):
                yValues.insert(0,int(fieldData[self.fieldSize-y-1][self.fieldSize-x-1]))
            field.insert(0,yValues)
    
        return field





class Pile:
    def __init__(self, pileName):
        self.pileName = pileName
        self.pile=self.getStartPile()
        self.shuffle()

    def __str__(self):

        #hvis en pile kaldes som en string, returneres en flot formateret sting med a
        string="\nStart bunken var "+self.pileName+"\nNuværende bunke:\n"
        for i in self.pile:
            string=string+str(i)+"\n"
        return string
    
    #bunke størrelse
    def __int__(self):
        return(len(self.pile))

    def getStartPile(self):
    
        #læser pile ind i pileData
        file=open(pathToGameDataFile("Piles",self.pileName), 'r', encoding="utf-8")
        pileData=file.read().split("\n")
        file.close()

        #skriver dataen over i lister, med piece navnet 
        pile=[]
        for line in pileData:
            lineDataSplit=line.split(" ", 1)

            for piece in range (  min( int(lineDataSplit[0]) , MAX_DUPES_IN_PILE)  ):
                pile.append(int(lineDataSplit[1]))

        return pile
    
    def drawPiece(self):
        '''
        fjern det øverste kort i bunken og returner det
        '''
        return self.pile.pop(0)
    

    def lookAtTop(self, amount=1):
        '''
        returnere de øverste kort af bunken
        '''
        return self.pile[:amount]
    
    def insertPiece(self, pieceIdOrPieceIdList, onTop = True):
        '''
        indsætter en string eller liste med strings i bunken enten i toppen eller bunden
        '''
        if type(pieceIdOrPieceIdList) == int:
            pieceList = [pieceIdOrPieceIdList]
        else:
            pieceList = pieceIdOrPieceIdList
        

        if onTop:
            self.pile[0:0] = pieceList
        else: 
            self.pile.extend(pieceList)
    
   
    def shuffle(self):
        '''
        bland bunken
        '''
        random.shuffle(self.pile)


if __name__ == '__main__':
    kort=Field(1)
    print(kort)

    pile=Pile("Default")
    print(pile)
    pass