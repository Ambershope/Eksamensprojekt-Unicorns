import random
from Database import pathToGameDataFile
from Constants import MAX_DUPES_IN_PILE

class Field:
    def __init__ (self, fieldId=0):
        self.fieldId=fieldId
        self.tileField=self.getStartField()

    #returnere en string med et flot formateret field
    def __str__ (self):
        tekst="\n"

        for y in range (self.fieldSize):
            for x in range (self.fieldSize):
                tekst += " " + str(self.tileField[x][y]) + " "
            tekst += "\n"

        return tekst
        
    def getStartField(self):
        #får field ind i fieldData
        file=open(pathToGameDataFile("Maps","Map"+str(self.fieldId)), 'r')
        fieldData=file.read().split("\n")
        file.close()

        #finder sidelængden på banen
        sizeX=len(fieldData)
        sizeY=len(fieldData[0])
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
                yValues.insert(0,int(fieldData[x][self.fieldSize-y-1]))
            field.insert(0,yValues)
        
        return field





class Pile:
    def __init__(self, pileName):
        self.pileName =pileName
        self.pile=self.getStartPile()
        self.shuffle()

    def __str__(self):
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
                pile.append(lineDataSplit[1])

        return pile
    
    #fjern det øverste kort i bunken og returner det
    def drawPiece(self):
        return self.pile.pop(0)
    
    #returnere de øverste kort af bunken
    def lookAtTop(self, amount=1):
        return self.pile[:amount]
    
    #indsætter en string eller liste med strings i bunken enten i toppen eller bunden
    def insertPiece(self, pieceNameStrOrList, onTop = True):

        if type(pieceNameStrOrList) == str:
            pieceList = [pieceNameStrOrList]
        else:
            pieceList = pieceNameStrOrList
        

        if onTop:
            self.pile[0:0] = pieceList
        else: 
            self.pile.extend(pieceList)
    
    #bland bunken
    def shuffle(self):
        random.shuffle(self.pile)


if __name__ == '__main__':
    kort=Field(1)
    print(kort)

    pile=Pile("Default")
    print(pile)
    pass