import pygame
import chessPieces
from config import *


class Board:
    def __init__(self,screen):
        
        self.pieces = [[None for x in range(8)] for y in range(8)] #Create an empty 2D array of size 8x8 [Row][Column]

        self.initialisePieces()
        self.screen = screen

        self.piecesString = createPiecesWString(self.pieces)

        self.blackKing = self.pieces[0][4]
        self.blackKingPosition = (0,4)

        self.whiteKing = self.pieces[7][4]
        self.whiteKingPosition = (7,4)

        self.checkedPosition = () 
        self.checkingPositions = [] #Positions of pieces which are causing check
        self.squareSelected = ()
        self.moveToPosition = ()
        self.playableSquares = []

        self.turn = "white"
        self.engineTeam = None

        self.activeThreads = []
        self.findingBestMove = [False,False] #findingBestMove/PlayedBestMove
        self.modeOption = 0

        self.fontBig = pygame.font.SysFont(None, 60)
        self.infoText = self.fontBig.render("", 1, (0, 0, 0))

    
    def updateBoard(self,squareSelected,moveToPosition,checkedPosition,playableSquares):
        for row in range(8):
            for column in range(8):
                if (row+column) % 2 == 0:
                    #Draw square of colour BOARDCOLOR1
                    pygame.draw.rect(self.screen,BOARDCOLOR1,
                                    pygame.Rect(column*SQUARESIZE,row*SQUARESIZE,SQUARESIZE,SQUARESIZE))
                else:
                    #Draw square of colour BOARDCOLOR2
                    pygame.draw.rect(self.screen,BOARDCOLOR2,
                                    pygame.Rect(column*SQUARESIZE,row*SQUARESIZE,SQUARESIZE,SQUARESIZE))
        
        #Highlighting
        if squareSelected != (): #Highlight the square selected
            pygame.draw.rect(self.screen,SELECTIONCOLOR,
                    pygame.Rect(squareSelected[1]*SQUARESIZE,squareSelected[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))
        
        if moveToPosition != (): #Highlight the square that was moved to
            pygame.draw.rect(self.screen,MOVECOLOR,
                    pygame.Rect(moveToPosition[1]*SQUARESIZE,moveToPosition[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))

        if checkedPosition != (): #Highlight the king square if in check
            pygame.draw.rect(self.screen,CHECKCOLOR,
                    pygame.Rect(checkedPosition[1]*SQUARESIZE,checkedPosition[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))

        for square in playableSquares: #Highlight all the squares of the moves a piece can make
            pygame.draw.circle(self.screen,SELECTIONCOLOR,
                    (square[1]*SQUARESIZE + SQUARESIZE/2,square[0]*SQUARESIZE + SQUARESIZE/2),SQUARESIZE/8,20)

            #if piece on square, make the playable square more visible
            if self.pieces[square[0]][square[1]] != None:
                
                pygame.draw.rect(self.screen,SELECTIONCOLOR,
                    pygame.Rect(square[1]*SQUARESIZE,square[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))

                if (square[0] + square[1]) % 2 == 0:
                    pygame.draw.circle(self.screen,BOARDCOLOR1,
                        (square[1]*SQUARESIZE + SQUARESIZE/2,square[0]*SQUARESIZE + SQUARESIZE/2),SQUARESIZE/2,40)
                else:
                    pygame.draw.circle(self.screen,BOARDCOLOR2,
                        (square[1]*SQUARESIZE + SQUARESIZE/2,square[0]*SQUARESIZE + SQUARESIZE/2),SQUARESIZE/2,40)

                                    

    def updatePieces(self):
        for row in self.pieces:
            for piece in row:
                if piece != None: #If there is a piece, draw it onto the screen
                    self.screen.blit(piece.image,pygame.Rect(piece.screenPosition[0],piece.screenPosition[1],SQUARESIZE,SQUARESIZE))

    def initialisePieces(self):
        #Black Pieces on First Row
        self.pieces[0] = [chessPieces.Rook(0,0,"black",SQUARESIZE),
                        chessPieces.Knight(0,1,"black",SQUARESIZE),
                        chessPieces.Bishop(0,2,"black",SQUARESIZE),
                        chessPieces.Queen(0,3,"black",SQUARESIZE),
                        chessPieces.King(0,4,"black",SQUARESIZE),
                        chessPieces.Bishop(0,5,"black",SQUARESIZE),
                        chessPieces.Knight(0,6,"black",SQUARESIZE),
                        chessPieces.Rook(0,7,"black",SQUARESIZE)
                        ]

        #White Pieces on Last Row
        self.pieces[7] = [chessPieces.Rook(7,0,"white",SQUARESIZE),
                        chessPieces.Knight(7,1,"white",SQUARESIZE),
                        chessPieces.Bishop(7,2,"white",SQUARESIZE),
                        chessPieces.Queen(7,3,"white",SQUARESIZE),
                        chessPieces.King(7,4,"white",SQUARESIZE),
                        chessPieces.Bishop(7,5,"white",SQUARESIZE),
                        chessPieces.Knight(7,6,"white",SQUARESIZE),
                        chessPieces.Rook(7,7,"white",SQUARESIZE)
                        ]
        #Pawns
        for column in range(8):
            self.pieces[1][column] = chessPieces.Pawn(1,column,"black",SQUARESIZE)
            self.pieces[6][column] = chessPieces.Pawn(6,column,"white",SQUARESIZE)

    def resetBoard(self):
        if self.activeThreads != []: #If there are any active threads, make sure they finish before you reset the board
            self.activeThreads[0].join()
        
        #Save the mode option before the contstructor is called
        modeOption = self.modeOption
        self.__init__(self.screen) #Call the constructor to reset the board
        self.modeOption = modeOption #Reload the modeOption attribute
        
        self.updateBoard(self.squareSelected,self.moveToPosition,self.checkedPosition,self.playableSquares) 
        self.updatePieces()

        #Change the engineTeam according to the modeOptoin
        if self.modeOption == 0:
            self.engineTeam = None
        elif self.modeOption == 1:
            self.engineTeam = "black"
        elif self.modeOption == 2:
            self.engineTeam = "white"
        elif self.modeOption == 3:
            self.engineTeam = self.turn

        
        self.infoText = self.fontBig.render("", 1, (0, 0, 0)) #Reset bottom text
        print("Board has been reset")
        
#For displaying the board in console using text
    def consoleDisplay(self):
        for row in self.pieces:
            for piece in row:
                if piece != None:
                    print(piece.pieceName+' ',end='')
                else:
                    print('     ',end='')
            print()
        print("-----------------------")
        

#Moving a piece(from, to)
    def movePiece(self,oldLocation,newLocation):
        oldRow = oldLocation[0]
        oldColumn = oldLocation[1]
        newRow = newLocation[0]
        newColumn = newLocation[1]


        oldScreenLocation = self.pieces[oldRow][oldColumn].screenPosition # old location as tuple (x,y)
        newScreenLocation = (newColumn*SQUARESIZE,newRow*SQUARESIZE) #[x,y]

        clock = pygame.time.Clock()

        #MAXFPS//MOVEMENTSPEED + 1, so that the piece will move within 1/MOVEMENTSPEED seconds
        for i in range(0,MAXFPS//MOVEMENTSPEED + 1):
            #xPos and yPos are the coordinates of the piece after each iteration of the for loop
            xPos = (newScreenLocation[0]-oldScreenLocation[0])*i/(MAXFPS//MOVEMENTSPEED) + oldScreenLocation[0]
            yPos = (newScreenLocation[1]-oldScreenLocation[1])*i/(MAXFPS//MOVEMENTSPEED) + oldScreenLocation[1]

            #Change the position and then draw the pieces again (the piece will now be in a sligtly different position)
            self.pieces[oldRow][oldColumn].screenPosition = [xPos,yPos]
            self.updateBoard(oldLocation,newLocation,(),[])
            self.updatePieces()
            pygame.display.flip()
            clock.tick(MAXFPS)
        
        self.pieces[oldRow][oldColumn].boardPosition = (newRow,newColumn)
        self.pieces[newRow][newColumn] = self.pieces[oldRow][oldColumn]
        self.pieces[oldRow][oldColumn] = None

        #Handle black pawn promotion if the pawn is moved to the end row
        if newRow == 7 and self.pieces[newRow][newColumn].pieceName == "b_pa":
            self.pieces[newRow][newColumn] = chessPieces.Queen(newRow,newColumn,"black",SQUARESIZE)

        #If a white pawn moves to the end row, turn it into a queen
        if newRow == 0 and self.pieces[newRow][newColumn].pieceName == "w_pa":
            self.pieces[newRow][newColumn] = chessPieces.Queen(newRow,newColumn,"white",SQUARESIZE)

        self.movePieceWithoutBoard(oldLocation,newLocation)


        self.updateBoard(oldLocation,newLocation,(),[])
        self.updatePieces()

        self.consoleDisplay()

    #Moves the piece without updating the visual aspect/window. This is used for looking ahead and validation
    def movePieceWithoutBoard(self,oldLocation,newLocation):

        oldRow = oldLocation[0]
        oldColumn = oldLocation[1]

        newRow = newLocation[0]
        newColumn = newLocation[1]

        if self.piecesString[oldRow][oldColumn] != None and self.piecesString[oldRow][oldColumn] == "w_ki":
            self.whiteKingPosition = newLocation


        if self.piecesString[oldRow][oldColumn] != None and self.piecesString[oldRow][oldColumn] == "b_ki":
            self.blackKingPosition = newLocation


        self.piecesString[newRow][newColumn] = self.piecesString[oldRow][oldColumn]
        self.piecesString[oldRow][oldColumn] = None

        if newRow == 7 and self.piecesString[newRow][newColumn] == "b_pa": #Black pawn promotion
            self.piecesString[newRow][newColumn] = "b_qu"

        if newRow == 0 and self.piecesString[newRow][newColumn] == "w_pa": #White pawn promotion
            self.piecesString[newRow][newColumn] = "w_qu"


def createPiecesWString(pieces):
    newPieces = [[None for x in range(8)] for y in range(8)]

    for row in range(0,8):
        for column in range(0,8):
            if pieces[row][column] != None:
                newPieces[row][column] = pieces[row][column].pieceName

    return newPieces
                
                
    




