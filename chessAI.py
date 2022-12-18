"""
Handling the AI moves.
"""
import random
import chessValidation

piece_score = {"ki": 0, "qu": 9, "ro": 5, "bi": 3, "kn": 3, "pa": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"w_kn": knight_scores,
                         "b_kn": knight_scores[::-1],
                         "w_bi": bishop_scores,
                         "b_bi": bishop_scores[::-1],
                         "w_qu": queen_scores,
                         "b_qu": queen_scores[::-1],
                         "w_ro": rook_scores,
                         "b_ro": rook_scores[::-1],
                         "w_pa": pawn_scores,
                         "b_pa": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def findBestMove(valid_moves,turn,board):
    global next_move
    random.shuffle(valid_moves)
    next_move = valid_moves[0]
    findMoveMiniMax(valid_moves,turn, DEPTH, -CHECKMATE, CHECKMATE,board)

    return next_move


def findMoveMiniMax(valid_moves,turn, depth, alpha, beta,board):
    global next_move
    if depth == 0:
        if turn == "white":
            return scoreBoard(turn,board)
        else:
            return -scoreBoard(turn,board)

    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        temp = board.piecesString[move[1][0]][move[1][1]]
        board.movePieceWithoutBoard(move[0],move[1])
        next_moves = chessValidation.getAllValidMoves("white" if turn == "black" else "black",board)
        score = -findMoveMiniMax(next_moves, "white" if turn == "black" else "black", depth - 1, -beta, -alpha,board)

        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        board.movePieceWithoutBoard(move[1],move[0])
        board.piecesString[move[1][0]][move[1][1]] = temp

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def scoreBoard(turn,board):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
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
                piece_position_score = 0
                if piece[2:] != "ki":
                    piece_position_score = piece_position_scores[piece][row][column]
                if piece[0] == "w":
                    score += piece_score[piece[2:]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[2:]] + piece_position_score

    return score


