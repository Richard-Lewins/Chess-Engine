#Check for stalemate
def checkForStalemate(turn,board):
    pieces = board.piecesString
    
    kingPosition = []

    #Get the king location
    if turn[0] == "w":
        kingPosition = board.whiteKingPosition
    else:
        kingPosition = board.blackKingPosition

    #Valid moves are found without getValidMoves function because we don't want ALL valid moves, but instead at least one
    #This makes this function more efficient
    staleMate = True

    for row in range(0,8):
        for column in range(0,8):
            if pieces[row][column] != None and pieces[row][column][0] == turn[0]:
                possibleMoves = getMoves((row,column),board)

                for move in possibleMoves:
                    #If there is already a piece here it stores it as temp to put it back
                    temp = pieces[move[0]][move[1]]
                    pawnPromotion = None

                    if row == 6 and pieces[row][column] == "b_pa":
                        pawnPromotion = "black"
                    
                    elif row == 1 and pieces[row][column] == "w_pa":
                        pawnPromotion = "white"


                    board.movePieceWithoutBoard((row,column),move)
                    if (row,column) == kingPosition: #If king is moved, use new king location
                        if not checkForCheck(move,board):
                            staleMate = False #As soon as a valid move is found, return 

                    elif not checkForCheck(kingPosition,board):
                        staleMate = False

                    board.movePieceWithoutBoard(move,(row,column))
                    pieces[move[0]][move[1]] = temp

                    #If pawn promoted, change piece back to pawn
                    if pawnPromotion == "black":
                        pieces[row][column] = "b_pa" 

                    elif pawnPromotion == "white":
                        pieces[row][column] = "w_pa"

                    if staleMate == False:
                        return staleMate

    return staleMate

def checkForCheck(kingPosition,board):

        pieces = board.piecesString
        row = kingPosition[0]
        column = kingPosition[1]
        possibleThreats = []
        checkingPieces = []

        cross = [[(row - i, column) for i in range(1, 8)], #Up
                 [(row + i, column) for i in range(1, 8)], #Down
                 [(row, column - i) for i in range(1, 8)], #Left
                 [(row, column + i) for i in range(1, 8)]] #Right

        diagonals = [[(row - i, column - i) for i in range(1,8)], #Up Left
                     [(row - i, column + i) for i in range(1,8)], #Up Right
                     [(row + i, column - i) for i in range(1,8)], #Down Left
                     [(row + i, column + i) for i in range(1,8)]] #Down Right

        knightDirections = [[(row-2,column-1)],[(row-1,column-2)], #Up Left
                            [(row-2,column+1)],[(row-1,column+2)], #Up Right
                            [(row+2,column-1)],[(row+1,column-2)], #Down Left
                            [(row+2,column+1)],[(row+1,column+2)]] #Down Right

        directions = cross + diagonals + knightDirections
        
        #Check If there are any pieces in "sight"
        for direction in directions:
            for square in direction:
                if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                    if pieces[square[0]][square[1]] != None:
                        if pieces[square[0]][square[1]][0] != pieces[row][column][0]: #If on same team
                            possibleThreats.append(square) 
                        break

        #See if any of these pieces can attack
        for position in possibleThreats:
            if kingPosition in getMoves(position,board):
                checkingPieces.append(position)

        return checkingPieces

#Returns list valid moves that a player in check can make (fromMove,toMove)
def outOfCheckMoves(kingPosition,checkingPositions,board):
    pieces = board.piecesString

    validMoves = []

    kingMoves = getMoves(kingPosition,board)
    kingTeam = pieces[kingPosition[0]][kingPosition[1]][0]

    #Check The King Possible Moves
    for move in kingMoves:
        temp = pieces[move[0]][move[1]]

        board.movePieceWithoutBoard(kingPosition,move)

        if checkForCheck(move,board) == []:
            validMoves.append((kingPosition,move))
            
        board.movePieceWithoutBoard(move,kingPosition) #Move Back
        pieces[move[0]][move[1]] = temp

    if len(checkingPositions) > 1: #If more than 1 pieces causing check, only option is to move king
        return validMoves

    kingRow = kingPosition[0]
    kingColumn = kingPosition[1]

    checkingRow = checkingPositions[0][0]
    checkingColumn = checkingPositions[0][1]

    positionsInBetween = []

    #If the checking piece is a knight, we don't need to consider the squares in between (knight can jump over)
    #Only consider the knight piece itself
    if pieces[checkingRow][checkingColumn][2:] == "kn":
        positionsInBetween.append((checkingRow,checkingColumn))

    else:
        rowChange = checkingRow - kingRow
        columnChange = checkingColumn - kingColumn
        row = kingRow
        column = kingColumn

        #Add all squares in between king and checking pieces to positionsInBetween (including checking pieces)
        while (row != checkingRow) or (column != checkingColumn):
            if rowChange != 0:
                row += int(rowChange/abs(rowChange))
            if columnChange != 0:
                column += int(columnChange/abs(columnChange))

            positionsInBetween.append((row,column))

    for position in positionsInBetween:
        row = position[0]
        column = position[1]
        possibleObstacles = [] #Possible pieces that could move in between the King and Checking Piece

        cross = [[(row - i, column) for i in range(1, 8)], #Up
                [(row + i, column) for i in range(1, 8)], #Down
                [(row, column - i) for i in range(1, 8)], #Left
                [(row, column + i) for i in range(1, 8)]] #Right

        diagonals = [[(row - i, column - i) for i in range(1,8)], #Up Left
                    [(row - i, column + i) for i in range(1,8)], #Up Right
                    [(row + i, column - i) for i in range(1,8)], #Down Left
                    [(row + i, column + i) for i in range(1,8)]] #Down Right

        knightDirections = [[(row-2,column-1)],[(row-1,column-2)], #Up Left
                    [(row-2,column+1)],[(row-1,column+2)], #Up Right
                    [(row+2,column-1)],[(row+1,column-2)], #Down Left
                    [(row+2,column+1)],[(row+1,column+2)]] #Down Right

        directions = cross + diagonals + knightDirections
        
        #If there any pieces of the same team that is in check in the area around
        #This is a piece that could possibly be used to obstruct the path between the king and the checking piece
        for direction in directions:
            for square in direction:
                if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                    if pieces[square[0]][square[1]] != None:
                        if pieces[square[0]][square[1]][0] == kingTeam and square!=kingPosition:
                            possibleObstacles.append(square) 
                        break
        
        #If the piece can move inbetween the king and the checking piece, add this to the list of possible moves
        for obstacle in possibleObstacles:
            if position in getMoves(obstacle,board):
                validMoves.append((obstacle,position))


    return validMoves


#General function to get the moves a piece can make
def getMoves(targetPiece,board):
    pieces = board.piecesString
    row = targetPiece[0]
    column = targetPiece[1]
    pieceType = pieces[row][column][2:]
    pieceTeam = pieces[row][column][0]

    if pieceType == "pa" and pieceTeam == 'w': #White Pawn
        return getMovesWhitePawn(targetPiece,board)

    elif pieceType == "pa" and pieceTeam == 'b': #Black Pawn
        return getMovesBlackPawn(targetPiece,board)

    elif pieceType == "ro": #Rook
       return  getMovesRook(targetPiece,board)

    elif pieceType == "kn": #Knight
        return  getMovesKnight(targetPiece,board)

    elif pieceType == "bi": #Bishop
        return getMovesBishop(targetPiece,board)

    elif pieceType == "qu": #Queen
        return getMovesQueen(targetPiece,board)

    elif pieceType == "ki": #King
        return getMovesKing(targetPiece,board)

#This gets the valid moves (get moves but makes sure illegal moves causing check etc is not caused)
def getValidMoves(targetPiece,board):
    pieces = board.piecesString
    pieceTeam = pieces[targetPiece[0]][targetPiece[1]][0]
    possibleSquares = getMoves(targetPiece,board)
    kingPosition = ()
    
    #Get the position of the king
    if pieceTeam == "w":
        kingPosition = board.whiteKingPosition
    else:
        kingPosition = board.blackKingPosition

    playableSquares = []
    for square in possibleSquares:

        #If there is already a piece here it stores it as temp to put it back
        temp = pieces[square[0]][square[1]] 
        # Initialize a variable to store the player color if a pawn promotion occurs on this move
        pawnPromotion = None
        
        # Check if a black or white pawn reaches the end of the board, if so, promote it to a queen
        if targetPiece[0] == 6 and pieces[targetPiece[0]][targetPiece[1]] == "b_pa":
            pawnPromotion = "black"
        
        elif targetPiece[0] == 1 and pieces[targetPiece[0]][targetPiece[1]] == "w_pa":
            pawnPromotion = "white"
        
        # Move the piece on the board without updating the board object
        board.movePieceWithoutBoard(targetPiece,square)

        if pieces[square[0]][square[1]][2:] == "ki":
            
            #If the King is the piece highlighted, make sure to checkForCheck with the NEW king position
            if not checkForCheck(square,board):
                playableSquares.append(square) #Add new square to playable square


        elif not checkForCheck(kingPosition,board):
            playableSquares.append(square) #Add new square to playable square
        
        #Move the piece back after it's checked (so the board is back to its original position)
        board.movePieceWithoutBoard(square,targetPiece)
        pieces[square[0]][square[1]] = temp

        #If there was pawn promotion, revert the piece back into a pawn
        if pawnPromotion == "black":
            pieces[targetPiece[0]][targetPiece[1]] = "b_pa" 

        elif pawnPromotion == "white":
            pieces[targetPiece[0]][targetPiece[1]] = "w_pa"

    return playableSquares

def getAllValidMoves(team,board):
    pieces = board.piecesString
    allValidMoves = []
    #Get all teh valid moves a certain team can make
    for row in range(0,8):
        for column in range(0,8):
            validMoves = []
            if pieces[row][column] != None and pieces[row][column][0] == team[0]:
                validMoves = getValidMoves((row,column),board)

            for move in validMoves:
                allValidMoves.append([(row,column),move])

    return allValidMoves

def getMovesKing(targetPiece,board):
    pieces = board.piecesString

    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]

    squares = [(row-2,column-1),(row-1,column-2), #Up Left
                (row-2,column+1),(row-1,column+2), #Up Right
                (row+2,column-1),(row+1,column-2), #Down Left
                (row+2,column+1),(row+1,column+2)] #Down Right
    
    for square in squares:
        if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                if pieces[square[0]][square[1]] == None or pieces[square[0]][square[1]][0] != pieces[row][column][0]:
                    possibleMoves.append(square)
    
    print(possibleMoves)
    return possibleMoves

def getMovesRook(targetPiece,board):
    pieces = board.piecesString

    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]
    
    cross = [[(row - i, column) for i in range(1, 8)], #Up
                [(row + i, column) for i in range(1, 8)], #Down
                [(row, column - i) for i in range(1, 8)], #Left
                [(row, column + i) for i in range(1, 8)]] #Right

    for direction in cross:
        for square in direction:
            if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                if pieces[square[0]][square[1]] == None:
                    possibleMoves.append(square)
                else:
                    if pieces[square[0]][square[1]][0] != pieces[row][column][0]:
                        #If on enemy team
                        possibleMoves.append(square) 
                    break
    
    
    return possibleMoves


def getMovesBishop(targetPiece,board):
    pieces = board.piecesString

    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]
    
    diagonals = [[(row - i, column - i) for i in range(1,8)], #Up Left
                    [(row - i, column + i) for i in range(1,8)], #Up Right
                    [(row + i, column - i) for i in range(1,8)], #Down Left
                    [(row + i, column + i) for i in range(1,8)]] #Down Right

    
    for direction in diagonals:
        for square in direction:
            if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                if pieces[square[0]][square[1]] == None:
                    possibleMoves.append(square)
                else:
                    if pieces[square[0]][square[1]][0] != pieces[row][column][0]:
                        #If on enemy team
                        possibleMoves.append(square) 
                    break
    
    
    return possibleMoves

def getMovesQueen(targetPiece,board):
    pieces = board.piecesString
    possibleMoves = []
    
    possibleMoves = getMovesBishop(targetPiece,board) +getMovesRook(targetPiece,board)

    return possibleMoves


def getMovesKing(targetPiece,board):
    pieces = board.piecesString

    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]

    squares = [(row-1,column-1),(row-1,column),(row-1,column+1), #Up (Left Middle Right)
                (row,column-1),(row,column+1),                    #Middle(Left Right)
                (row+1,column-1),(row+1,column),(row+1,column+1)]  #Bottom(Left Middle Right)
    
    for square in squares:
        if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                if pieces[square[0]][square[1]] == None or pieces[square[0]][square[1]][0] != pieces[row][column][0]:
                    possibleMoves.append(square)

    return possibleMoves


def getMovesKnight(targetPiece,board):
    pieces = board.piecesString
    
    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]

    squares = [(row-2,column-1),(row-1,column-2), #Up Left
                (row-2,column+1),(row-1,column+2), #Up Right
                (row+2,column-1),(row+1,column-2), #Down Left
                (row+2,column+1),(row+1,column+2)] #Down Right(
    for square in squares:
        if square[0] >= 0 and square[0]<=7 and square[1] >=0 and square[1] <=7:
                if pieces[square[0]][square[1]] == None or pieces[square[0]][square[1]][0] != pieces[row][column][0]:
                    possibleMoves.append(square)

    
    return possibleMoves

def getMovesWhitePawn(targetPiece,board):
    pieces = board.piecesString

    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]

        #if on the top most row, it cannot move further
    if row == 0:
        return possibleMoves

    #Capturing Diagonally (Right)
    
    if column != 7:
        if pieces[row - 1][column+1] != None and pieces[row - 1][column+1][0] != 'w':
            possibleMoves.append((row-1,column+1))

    #Capturing Diagonally (Left)
    if column != 0:
        if pieces[row - 1][column-1] != None and pieces[row - 1][column-1][0] != 'w':
            possibleMoves.append((row-1,column-1))
    
    #It can move 1 piece upwards if no other pieces
    if pieces[row - 1][column] == None:
        possibleMoves.append((row-1,column))
    else:
        return possibleMoves
    
    #If on 7th row, it can move 2 spaces
    if row == 6:
        if pieces[row - 2][column] == None:
            possibleMoves.append((row-2,column))
    
    return possibleMoves

def getMovesBlackPawn(targetPiece,board):
    pieces = board.piecesString
    possibleMoves = []
    row = targetPiece[0]
    column = targetPiece[1]


    #if on the bottom most row, it cannot move further
    if row == 7:
        return possibleMoves

    #Capturing Diagonally (Right)
    if column != 7:
        if pieces[row + 1][column+1] != None and pieces[row + 1][column+1][0] != 'b':
            possibleMoves.append((row+1,column+1))

    #Capturing Diagonally (Left)
    if column != 0:
        if pieces[row + 1][column-1] != None and pieces[row + 1][column-1][0] != 'b':
            possibleMoves.append((row+1,column-1))
    
    #It can move 1 piece down if no other pieces
    if pieces[row + 1][column] == None:
        possibleMoves.append((row+1,column))
    else:
        return possibleMoves
    
    #If on 2nd row, it can move 2 spaces
    if row == 1:
        if pieces[row + 2][column] == None:
            possibleMoves.append((row+2,column))
    
    return possibleMoves