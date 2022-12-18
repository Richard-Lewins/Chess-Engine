import pygame
import chessPieces
from config import *

MAXFPS = 60 #Change to max FPS
class Board:
    def __init__(self,screen):
        
        self.pieces = [[None for x in range(8)] for y in range(8)] #Create an empty 2D array of size 8x8 [Row][Column]

        self.screen = screen
        self.initialisePieces()

        self.piecesString = createPiecesWString(self.pieces)

        self.blackKing = self.pieces[0][4]
        self.blackKingPosition = [0,4]

        self.whiteKing = self.pieces[7][4]
        self.whiteKingPosition = [7,4]

        self.checkedPosition = [] 
        self.checkingPositions = [] #Positions of pieces which are causing check

        self.turn = "white"

    
    def updateBoard(self,screen,squareSelected,moveToPosition,checkedPosition,playableSquares):
        for row in range(8):
            for column in range(8):
                if (row+column) % 2 == 0:
                    pygame.draw.rect(screen,BOARDCOLOR1,
                                    pygame.Rect(column*SQUARESIZE,row*SQUARESIZE,SQUARESIZE,SQUARESIZE))
                else:
                    pygame.draw.rect(screen,BOARDCOLOR2,
                                    pygame.Rect(column*SQUARESIZE,row*SQUARESIZE,SQUARESIZE,SQUARESIZE))
        
        #Highlighting
        if squareSelected != []:
            pygame.draw.rect(screen,SELECTIONCOLOR,
                    pygame.Rect(squareSelected[1]*SQUARESIZE,squareSelected[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))
        
        if moveToPosition != []:
            pygame.draw.rect(screen,MOVECOLOR,
                    pygame.Rect(moveToPosition[1]*SQUARESIZE,moveToPosition[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))

        if checkedPosition != []:
            pygame.draw.rect(screen,CHECKCOLOR,
                    pygame.Rect(checkedPosition[1]*SQUARESIZE,checkedPosition[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))

        for square in playableSquares:
            pygame.draw.circle(screen,SELECTIONCOLOR,
                    (square[1]*SQUARESIZE + SQUARESIZE/2,square[0]*SQUARESIZE + SQUARESIZE/2),SQUARESIZE/8,20)

            #if piece on square, make the playable square more visible
            if self.pieces[square[0]][square[1]] != None:
                
                pygame.draw.rect(screen,SELECTIONCOLOR,
                    pygame.Rect(square[1]*SQUARESIZE,square[0]*SQUARESIZE,SQUARESIZE,SQUARESIZE))

                if (square[0] + square[1]) % 2 == 0:
                    pygame.draw.circle(screen,BOARDCOLOR1,
                        (square[1]*SQUARESIZE + SQUARESIZE/2,square[0]*SQUARESIZE + SQUARESIZE/2),SQUARESIZE/2,40)
                else:
                    pygame.draw.circle(screen,BOARDCOLOR2,
                        (square[1]*SQUARESIZE + SQUARESIZE/2,square[0]*SQUARESIZE + SQUARESIZE/2),SQUARESIZE/2,40)

                                    

    def updatePieces(self,screen):
        for row in self.pieces:
            for piece in row:
                if piece != None:
                    screen.blit(piece.image,pygame.Rect(piece.screenPosition[0],piece.screenPosition[1],SQUARESIZE,SQUARESIZE))

    def initialisePieces(self):
        #Black Pieces on First Row
        self.pieces[0] = [chessPieces.Rook(0,0,"black",SQUARESIZE,"b_rook.png"),
                        chessPieces.Knight(0,1,"black",SQUARESIZE,"b_knight.png"),
                        chessPieces.Bishop(0,2,"black",SQUARESIZE,"b_bishop.png"),
                        chessPieces.Queen(0,3,"black",SQUARESIZE,"b_queen.png"),
                        chessPieces.King(0,4,"black",SQUARESIZE,"b_king.png"),
                        chessPieces.Bishop(0,5,"black",SQUARESIZE,"b_bishop.png"),
                        chessPieces.Knight(0,6,"black",SQUARESIZE,"b_knight.png"),
                        chessPieces.Rook(0,7,"black",SQUARESIZE,"b_rook.png")
                        ]

        #White Pieces on Last Row
        self.pieces[7] = [chessPieces.Rook(7,0,"white",SQUARESIZE,"w_rook.png"),
                        chessPieces.Knight(7,1,"white",SQUARESIZE,"w_knight.png"),
                        chessPieces.Bishop(7,2,"white",SQUARESIZE,"w_bishop.png"),
                        chessPieces.Queen(7,3,"white",SQUARESIZE,"w_queen.png"),
                        chessPieces.King(7,4,"white",SQUARESIZE,"w_king.png"),
                        chessPieces.Bishop(7,5,"white",SQUARESIZE,"w_bishop.png"),
                        chessPieces.Knight(7,6,"white",SQUARESIZE,"w_knight.png"),
                        chessPieces.Rook(7,7,"white",SQUARESIZE,"w_rook.png")
                        ]
        #Pawns
        for column in range(8):
            self.pieces[1][column] = chessPieces.Pawn(1,column,"black",SQUARESIZE,"b_pawn.png")
            self.pieces[6][column] = chessPieces.Pawn(6,column,"white",SQUARESIZE,"w_pawn.png")

        

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

        oldScreenLocation = self.pieces[oldLocation[0]][oldLocation[1]].screenPosition
        newScreenLocation = [newLocation[1]*SQUARESIZE,newLocation[0]*SQUARESIZE] #[x,y]

        clock = pygame.time.Clock()

        #MAXFPS//4 + 1, so that the piece will move within 0.25 seconds
        for i in range(0,MAXFPS//4 + 1):
            #xPos and yPos are the coordinates of the piece after each iteration of the for loop
            xPos = (newScreenLocation[0]-oldScreenLocation[0])*i/(MAXFPS//4) + oldScreenLocation[0]
            yPos = (newScreenLocation[1]-oldScreenLocation[1])*i/(MAXFPS//4) + oldScreenLocation[1]

            self.pieces[oldLocation[0]][oldLocation[1]].screenPosition = [xPos,yPos]
            self.updateBoard(self.screen,oldLocation,newLocation,[],[])
            self.updatePieces(self.screen)
            pygame.display.flip()
            clock.tick(MAXFPS)
        
        self.pieces[oldLocation[0]][oldLocation[1]].boardPosition = [newLocation[0],newLocation[1]]
        self.pieces[newLocation[0]][newLocation[1]] = self.pieces[oldLocation[0]][oldLocation[1]]
        self.pieces[oldLocation[0]][oldLocation[1]] = None
        self.movePieceWithoutBoard(oldLocation,newLocation)


        self.updateBoard(self.screen,oldLocation,newLocation,[],[])
        self.updatePieces(self.screen)

        self.consoleDisplay()

    def movePieceWithoutBoard(self,oldLocation,newLocation):

        row = oldLocation[0]
        column = oldLocation[1]

        if self.piecesString[row][column] != None and self.piecesString[row][column] == "w_ki":
            self.whiteKingPosition = newLocation


        if self.piecesString[row][column] != None and self.piecesString[row][column] == "b_ki":
            self.blackKingPosition = newLocation


        self.piecesString[newLocation[0]][newLocation[1]] = self.piecesString[oldLocation[0]][oldLocation[1]]
        self.piecesString[oldLocation[0]][oldLocation[1]] = None

def createPiecesWString(pieces):
    newPieces = [[None for x in range(8)] for y in range(8)]

    for row in range(0,8):
        for column in range(0,8):
            if pieces[row][column] != None:
                newPieces[row][column] = pieces[row][column].pieceName

    return newPieces
                
                
    





    


