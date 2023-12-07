import pygame
import chessBoard
import chessValidation
import chessMenu
import chessAI
from config import *
import random
import threading


def main():
    #
    pygame.init()
    pygame.display.set_caption('CS NEA Chess Engine')
    screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    clock = pygame.time.Clock()
    screen.fill(BGCOLOR)

    board = chessBoard.Board(screen)

    board.updateBoard(board.squareSelected,board.moveToPosition,board.checkedPosition,board.playableSquares) 
    board.updatePieces() #Moved screen parameter to Board

    font = pygame.font.SysFont(None, 30) #Font used throughout the menu

    #Create the mode dropbox object
    modeDropbox = chessMenu.OptionBox(
        550, 40, 200, 40, (150, 150, 150), (100, 200, 255), font, 
        ["Player vs Player", "Player vs Black", "Player vs White","Bot vs Bot"])
    
    #Create the difficulty dropbox object
    diffDropbox = chessMenu.OptionBox(
        550, 300, 200, 40, (150, 150, 150), (100, 200, 255), font, 
        ["Easy", "Medium", "Hard"])
    
    #Create the reset button object
    resetButton = chessMenu.button(
        670, 526, 100, 40, (150, 150, 150), (250, 100, 100), font, 
        "Reset",board.resetBoard)
    

    DEPTH = 1
    

    running = True
    
    bestMove = [None]
    while running:
        if board.turn == board.engineTeam:
            #If it's the board.engineTeam's turn, call the runEngine function to find the bestMove
            runEngine(board,bestMove,DEPTH)
            
                          
            
        eventList =pygame.event.get()
        for e in eventList:
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                screen.fill(BGCOLOR)
                board.updateBoard(board.squareSelected,board.moveToPosition,board.checkedPosition,board.playableSquares) 
                board.updatePieces()                
                modeDropbox.draw(screen)
                diffDropbox.draw(screen)
                if board.findingBestMove == [False,False] and board.modeOption != 3: 
                    #If it's not finding the best move or waiting to update
                    #Handle the click event
                    handleClickEvent(location,board)

        
        #Each tick, see if the state of the mode dropbox has changed
        #If it has cahnged, change the board.modeOption accordingly

        #mode 0 is player vs player
        #mode 1 is player vs the computer and the computer is black
        #mode 2 is player vs the comptuer and the computer is white
        #mode 3 is computer vs computer
        boxUpdate = modeDropbox.update(eventList)
        if boxUpdate >= 0:
            if boxUpdate == 0:
                print("Mode Changed to Player vs Player")
                board.modeOption = 0
                board.engineTeam = None
                
            elif boxUpdate ==1:
                print("Mode Changed to Player vs Computer (Computer is Black)")
                board.modeOption = 1
                board.engineTeam = "black"

            elif boxUpdate ==2:
                print("Mode Changed to Player vs Computer (Computer is White)")
                board.modeOption = 2
                board.engineTeam = "white"
            elif boxUpdate ==3:
                print("Mode Changed to Computer vs Computer")
                board.modeOption = 3
                board.engineTeam = board.turn
            screen.fill(BGCOLOR)
            board.updateBoard(board.squareSelected,board.moveToPosition,board.checkedPosition,board.playableSquares) 
            board.updatePieces()

        modeDropbox.draw(screen)
        
        #Each tick, see if the state of the difficulty dropbox has changed
        #If it has changed, change the DEPTH accordingly
        difficultyUpdate = diffDropbox.update(eventList)
        if difficultyUpdate >= 0:
            if difficultyUpdate == 0:
                print("Difficulty: Easy")
                DEPTH = 1
                
            elif difficultyUpdate  ==1:
                print("Difficulty: Medium")
                DEPTH = 2

            elif difficultyUpdate  ==2:
                print("Difficulty: Hard")
                DEPTH = 3

            screen.fill(BGCOLOR)
            board.updateBoard(board.squareSelected,board.moveToPosition,board.checkedPosition,board.playableSquares) 
            board.updatePieces()
        
        diffDropbox.draw(screen)

        resetButton.update(eventList)
        resetButton.draw(screen)
        screen.blit(board.infoText, board.infoText.get_rect(center = (300,549)))
        
        clock.tick(MAXFPS)
        pygame.display.flip()



def handleClickEvent(location,board):
    columnClicked = location[0]//SQUARESIZE 
    rowClicked = location[1]//SQUARESIZE 

    if columnClicked <= 7 and rowClicked <= 7: #If the click is on the board

        #If the user clicks the already selected square, deselect it
        if board.squareSelected == (rowClicked,columnClicked): 
            board.squareSelected = ()
            board.moveToPosition = ()
            board.playableSquares=[]

        #If the user clicks a new square, move to that position (if possible)
        #If the user clicks on a piece of the same team, change that piece to selected piece
        elif board.squareSelected != () and board.moveToPosition == (): 

            if board.pieces[rowClicked][columnClicked] != None:
                if board.pieces[rowClicked][columnClicked].team == board.turn:
                    board.squareSelected = (rowClicked,columnClicked)
                    board.playableSquares = chessValidation.getValidMoves(board.squareSelected,board)
                    print("Playable Squares:",board.playableSquares)


            
            if (rowClicked,columnClicked) in board.playableSquares:
                #If the square clicked is a playable square,  move the piece to this square
                board.moveToPosition = (rowClicked,columnClicked)
                board.checkedPosition = ()
                board.playableSquares = []
                board.movePiece(board.squareSelected,board.moveToPosition)
                print("WhiteKingPos:",board.whiteKingPosition)
                print("BlackKingPos:",board.blackKingPosition)
                print(chessAI.scoreBoard("white",board))

                print("White Check:",chessValidation.checkForCheck(board.whiteKingPosition,board))
                print("Black Check:",chessValidation.checkForCheck(board.blackKingPosition,board))

                if board.turn == "white":
                    board.turn = "black"
                    board.checkingPositions = chessValidation.checkForCheck(board.blackKingPosition,board)
                    #Check if the board is in check
                    if board.checkingPositions:
                        board.checkedPosition = board.blackKingPosition

                        outOfCheckMoves = chessValidation.outOfCheckMoves(board.checkedPosition,board.checkingPositions,board)                                  
                        print("Valid Moves:",outOfCheckMoves)
                        #If there are no moves to get out of check, it's checkmate
                        if not outOfCheckMoves:
                            print("CHECKMATE, White Wins")
                            #Update bottom text
                            board.infoText = board.fontBig.render("CHECKMATE, White Wins", 1, (0, 0, 0))
                    #If it's not check, but there are no moves, it's stalemate
                    elif chessValidation.checkForStalemate(board.turn,board):
                        print("STALEMATE, Draw")
                        #Update bottom text
                        board.infoText = board.fontBig.render("STALEMATE, Draw", 1, (0, 0, 0))

                else:
                    #Repeat for the white team
                    board.turn = "white"
                    board.checkingPositions = chessValidation.checkForCheck(board.whiteKingPosition,board)
                    if board.checkingPositions:
                        board.checkedPosition = board.whiteKingPosition

                        outOfCheckMoves = chessValidation.outOfCheckMoves(board.checkedPosition,board.checkingPositions,board)                                  
                        print("Valid Moves:",outOfCheckMoves)
                        if not outOfCheckMoves:
                            print("CHECKMATE,Black Wins")
                            board.infoText = board.fontBig.render("CHECKMATE, Black Wins", 1, (0, 0, 0))
                    
                    elif chessValidation.checkForStalemate(board.turn,board):
                        print("STALEMATE, Draw")
                        board.infoText = board.fontBig.render("STALEMATE, Draw", 1, (0, 0, 0))
                    
                

        #If there is nothing selected, select (if correct turn)
        else:
            if board.pieces[rowClicked][columnClicked] != None and board.pieces[rowClicked][columnClicked].team  == board.turn:
                board.squareSelected = (rowClicked,columnClicked)

                board.playableSquares = chessValidation.getValidMoves(board.squareSelected,board)
                print("Playable Squares: ",board.playableSquares)

                board.moveToPosition = ()

        board.updateBoard(board.squareSelected,board.moveToPosition,board.checkedPosition,board.playableSquares)
        board.updatePieces()

def runEngine(board,bestMove,DEPTH):
    if board.findingBestMove == [False,False]:
        #[FALSE,FALSE] means that 1) a move is not being searched for yet and 2) there are no moves to be made
        #This is used because of threading
        validMoves = chessValidation.getAllValidMoves(board.engineTeam,board)
        if validMoves:
            board.checkedPosition = ()
            board.findingBestMove[0] = True #Starts finding process
            board.findingBestMove[1] = True
            random.shuffle(validMoves)
            bestMove[0] = validMoves[0]
            #Create the thread to find the move
            findMoveThread = threading.Thread(target=chessAI.findBestMove,args=
                                    (validMoves,board.engineTeam,board,bestMove,board.findingBestMove,DEPTH))
            findMoveThread.daemon = True
            #Append the thread to the board.activeThreads to keep track of it
            board.activeThreads.append(findMoveThread)
            findMoveThread.start()

    elif board.findingBestMove == [False,True]:
        #If a move is not being found, but there is a move to be made
        #Make the move
        board.activeThreads.pop()
        board.movePiece(bestMove[0][0],bestMove[0][1])
        print("WhiteKingPos:",board.whiteKingPosition)
        print("BlackKingPos:",board.blackKingPosition)

        board.findingBestMove[1] = False
        if board.turn == "white":
            board.turn = "black"
            #Check for check
            board.checkingPositions = chessValidation.checkForCheck(board.blackKingPosition,board)
            if board.checkingPositions:
                board.checkedPosition = board.blackKingPosition

                #If there are no moves to get out of check, it's checkmate
                outOfCheckMoves = chessValidation.outOfCheckMoves(board.checkedPosition,board.checkingPositions,board)                                  
                print("Valid Moves:",outOfCheckMoves)
                if not outOfCheckMoves:
                    print("CHECKMATE, White Wins")
                    board.infoText = board.fontBig.render("CHECKMATE, White Wins", 1, (0, 0, 0))
            #If there are no moves, and it's not check, it's stalemate
            elif chessValidation.checkForStalemate(board.turn,board):
                print("STALEMATE, Draw")
                board.infoText = board.fontBig.render("STALEMATE, Draw", 1, (0, 0, 0))

        else:
            #repeat for white team
            board.turn = "white"
            board.checkingPositions = chessValidation.checkForCheck(board.whiteKingPosition,board)
            if board.checkingPositions:
                board.checkedPosition = board.whiteKingPosition

                outOfCheckMoves = chessValidation.outOfCheckMoves(board.checkedPosition,board.checkingPositions,board)                                  
                print("Valid Moves:",outOfCheckMoves)
                if not outOfCheckMoves:
                    print("CHECKMATE,Black Wins")
                    board.infoText = board.fontBig.render("CHECKMATE, Black Wins", 1, (0, 0, 0))
            
            elif chessValidation.checkForStalemate(board.turn,board):
                print("STALEMATE, Draw")
                board.infoText = board.fontBig.render("STALEMATE, Draw", 1, (0, 0, 0))
                
        board.updateBoard(board.squareSelected,board.moveToPosition,board.checkedPosition,board.playableSquares)
        board.updatePieces()

        if board.modeOption == 3:
            board.engineTeam = board.turn


main() #Call the main function
