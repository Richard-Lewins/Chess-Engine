import time
import chessValidation
from config import *

pieceScores = {"ki": 0, "qu": 9, "ro": 5, "bi": 3, "kn": 3, "pa": 1}

knightScores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishopScores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rookScores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queenScores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawnScores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.25, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.25],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piecePositionScores = {"w_kn": knightScores,
                         "b_kn": knightScores[::-1],
                         "w_bi": bishopScores,
                         "b_bi": bishopScores[::-1],
                         "w_qu": queenScores,
                         "b_qu": queenScores[::-1],
                         "w_ro": rookScores,
                         "b_ro": rookScores[::-1],
                         "w_pa": pawnScores,
                         "b_pa": pawnScores[::-1]}

CHECKMATE = 1000
STALEMATE = 0



def findBestMove(validMoves,turn,board,nextMove,findingBestMove,DEPTH):
    startTime = time.time()
    findMoveMiniMax(validMoves,nextMove,turn, DEPTH,DEPTH, -CHECKMATE, CHECKMATE,board)
    print("--- %s seconds ---" % (time.time() - startTime))
    findingBestMove[0] = False
    return nextMove


def findMoveMiniMax(validMoves,nextMove,turn, depth, MAXDEPTH, alpha, beta,board):

    # Check if the depth limit has been reached, if so, return the score of the board for the current player
    if depth == 0:
        if turn == "white":
            return scoreBoard(turn,board)
        else:
            return -scoreBoard(turn,board)

    maxScore = -CHECKMATE

    # Iterate through all valid moves to evaluate each possible move
    for move in validMoves:

        # Save the original piece that may be captured by this move
        temp = board.piecesString[move[1][0]][move[1][1]]

        # Initialize a variable to store the player color if a pawn promotion occurs on this move
        pawnPromotion = None

        # Check if a black or white pawn reaches the end of the board, if so, promote it to a queen
        if move[0][0] == 6 and board.piecesString[move[0][0]][move[0][1]] == "b_pa":
            pawnPromotion = "black"
        
        elif move[0][0] == 1 and board.piecesString[move[0][0]][move[0][1]] == "w_pa":
            pawnPromotion = "white"

        # Move the piece on the board without updating the board object
        board.movePieceWithoutBoard(move[0],move[1])
        nextMoves = chessValidation.getAllValidMoves("white" if turn == "black" else "black",board)

        # Recursively evaluate the opponent player's moves and return the negated score
        # This minimises their score
        score = -findMoveMiniMax(nextMoves,nextMove, "white" if turn == "black" else "black", depth - 1,MAXDEPTH, -beta, -alpha,board)

        # Check if the score is greater than the current maximum score for the current player's turn
        # If so, update the maximum score and store the move as the best move if we are at the maximum depth
        if score > maxScore:
            maxScore = score
            if depth == MAXDEPTH:
                nextMove[0] = move
        # Undo the move to revert the board back to its original state
        board.movePieceWithoutBoard(move[1],move[0])
        board.piecesString[move[1][0]][move[1][1]] = temp

         # Check if a pawn promotion occurred on this move, if so, revert the piece type accordingly
        if pawnPromotion == "black": 
            board.piecesString[move[0][0]][move[0][1]] = "b_pa" 

        elif pawnPromotion == "white":
            board.piecesString[move[0][0]][move[0][1]] = "w_pa"

        # Update alpha with the maximum score if it is greater than the current alpha value
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
        # If alpha is greater than or equal to beta, exit the loop because the best move for this 'branch' was found
    return maxScore


def scoreBoard(turn,board):

    #Score the board
    #Positive is good for white, and negative is good for black
    kingPosition = board.whiteKingPosition if turn == "white" else board.blackKingPosition
    
    checkingPositions = chessValidation.checkForCheck(kingPosition,board)
    if checkingPositions:
        if not chessValidation.outOfCheckMoves(kingPosition,checkingPositions,board):
            if turn == "white":
                return -CHECKMATE  # black wins
            else:
                return CHECKMATE  # white wins

    elif chessValidation.checkForStalemate(turn,board):
        return STALEMATE
        
    score = 0
    for row in range(0,8):
        for column in range(0,8):
            piece = board.piecesString[row][column]
            if piece != None:
                positionScore = 0
                #Add each piece, and there location scores to the total.
                if piece[2:] != "ki":
                    positionScore = piecePositionScores[piece][row][column]
                if piece[0] == "w":
                    score += pieceScores[piece[2:]] + positionScore
                if piece[0] == "b":
                    score -= pieceScores[piece[2:]] + positionScore

    return score


