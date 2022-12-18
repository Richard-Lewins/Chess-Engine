import pygame
import chessBoard
import chessValidation
import chessAI
from config import *
import time



def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    clock = pygame.time.Clock()
    screen.fill(BGCOLOR)
    squareSelected = [] #row,column
    moveToPosition = [] #row,column
    playableSquares = []

    board = chessBoard.Board(screen)

    board.updateBoard(screen,squareSelected,moveToPosition,[],playableSquares) 
    board.updatePieces(screen) #Moved screen parameter to Board
    

    running = True
    while running:
        if board.turn == "black":
            validMoves = chessValidation.getAllValidMoves("black",board)
            if validMoves:
                bestMove = chessAI.findBestMove(validMoves,"black",board)
                board.movePiece(bestMove[0],bestMove[1])
                print("WhiteKingPos:",board.whiteKingPosition)
                print("BlackKingPos:",board.blackKingPosition)
                board.turn = "white"
            else:
                print("CHECKMATE, White Wins")
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                columnClicked = location[0]//SQUARESIZE 
                rowClicked = location[1]//SQUARESIZE 

                if columnClicked <= 7 and rowClicked <= 7: #If the click is on the board

                    #If the user clicks the already selected square, deselect it
                    if squareSelected == [rowClicked,columnClicked]: 
                        squareSelected = [] 
                        moveToPosition = []
                        playableSquares=[]

                    #If the user clicks a new square, move to that position (if possible)
                    #If the user clicks on a piece of the same team, change that piece to selected piece
                    elif squareSelected != [] and moveToPosition == []: 
                        
                        if board.pieces[rowClicked][columnClicked] != None:
                            if board.pieces[rowClicked][columnClicked].team == board.turn:
                                squareSelected = [rowClicked,columnClicked]
                                playableSquares = chessValidation.getValidMoves(squareSelected,board)
                                print("Playable Squares:",playableSquares)


                        
                        if [rowClicked,columnClicked] in playableSquares:
                            moveToPosition = [rowClicked,columnClicked]
                            board.checkedPosition = [] 
                            playableSquares = []
                            board.movePiece(squareSelected,moveToPosition)
                            print("WhiteKingPos:",board.whiteKingPosition)
                            print("BlackKingPos:",board.blackKingPosition)

                            startTime = time.time()

                            print("White Check:",chessValidation.checkForCheck(board.whiteKingPosition,board))
                            print("Black Check:",chessValidation.checkForCheck(board.blackKingPosition,board))

                            if board.turn == "white":
                                board.turn = "black"
                                board.checkingPositions = chessValidation.checkForCheck(board.blackKingPosition,board)
                                if board.checkingPositions:
                                    board.checkedPosition = board.blackKingPosition

                                    outOfCheckMoves = chessValidation.outOfCheckMoves(board.checkedPosition,board.checkingPositions,board)                                  
                                    print("Valid Moves:",outOfCheckMoves)
                                    if not outOfCheckMoves:
                                        print("CHECKMATE, White Wins")
                                
                                elif chessValidation.checkForStalemate(board.turn,board):
                                    print("STALEMATE, Draw")

                            else:
                                board.turn = "white"
                                board.checkingPositions = chessValidation.checkForCheck(board.whiteKingPosition,board)
                                if board.checkingPositions:
                                    board.checkedPosition = board.whiteKingPosition

                                    outOfCheckMoves = chessValidation.outOfCheckMoves(board.checkedPosition,board.checkingPositions,board)                                  
                                    print("Valid Moves:",outOfCheckMoves)
                                    if not outOfCheckMoves:
                                        print("CHECKMATE,Black Wins")
                                
                                elif chessValidation.checkForStalemate(board.turn,board):
                                    print("STALEMATE, Draw")
                                
                            
                            endTime = time.time()
                            runTime = endTime - startTime


                            print("Time:",runTime)

                    #If there is nothing selected, select (if correct turn)
                    else:
                        if board.pieces[rowClicked][columnClicked] != None and board.pieces[rowClicked][columnClicked].team  == board.turn:
                            squareSelected = [rowClicked,columnClicked]

                            playableSquares = chessValidation.getValidMoves(squareSelected,board)
                            print("Playable Squares: ",playableSquares)

                            moveToPosition = []

                    board.updateBoard(screen,squareSelected,moveToPosition,board.checkedPosition,playableSquares)
                    board.updatePieces(screen)


                    


        
        clock.tick(MAXFPS)
        pygame.display.flip()

main()