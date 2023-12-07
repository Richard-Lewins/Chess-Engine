import pygame

class Piece:
    def __init__(self,row,column,team,size):
        self.boardPosition = (row,column)
        self.screenPosition = (column*size,row*size) #Screenposition would be the boardposition multiplied by the size of each square.
        self.team = team
        self.image = None


#For each of the child clases, the image will be loaded within the constructor
#The piece name is also defined in the constructor
class Pawn(Piece):
    def __init__(self,row,column,team,size):
        super().__init__(row,column,team,size)

        if team == "black": 
            self.image = pygame.transform.scale(pygame.image.load("Images/b_pawn.png"), (size,size))
            self.pieceName = "b_pa"
        elif team == "white":
            self.image = pygame.transform.scale(pygame.image.load("Images/w_pawn.png"), (size,size))
            self.pieceName = "w_pa"            



class Queen(Piece):
    def __init__(self,row,column,team,size):
        super().__init__(row,column,team,size)

        if team == "black": 
            self.image = pygame.transform.scale(pygame.image.load("Images/b_queen.png"), (size,size))
            self.pieceName = "b_qu"
        elif team == "white":
            self.image = pygame.transform.scale(pygame.image.load("Images/w_queen.png"), (size,size))
            self.pieceName = "w_qu"          
        

class Rook(Piece):
    def __init__(self,row,column,team,size):
        super().__init__(row,column,team,size)

        if team == "black": 
            self.image = pygame.transform.scale(pygame.image.load("Images/b_rook.png"), (size,size))
            self.pieceName = "b_ro"
        elif team == "white":
            self.image = pygame.transform.scale(pygame.image.load("Images/w_rook.png"), (size,size))
            self.pieceName = "w_ro"  


class Bishop(Piece):
    def __init__(self,row,column,team,size):
        super().__init__(row,column,team,size)

        if team == "black": 
            self.image = pygame.transform.scale(pygame.image.load("Images/b_bishop.png"), (size,size))
            self.pieceName = "b_bi"
        elif team == "white":
            self.image = pygame.transform.scale(pygame.image.load("Images/w_bishop.png"), (size,size))
            self.pieceName = "w_bi"  

   

class Knight(Piece):
    def __init__(self,row,column,team,size):
        super().__init__(row,column,team,size)

        if team == "black": 
            self.image = pygame.transform.scale(pygame.image.load("Images/b_knight.png"), (size,size))
            self.pieceName = "b_kn"
        elif team == "white":
            self.image = pygame.transform.scale(pygame.image.load("Images/w_knight.png"), (size,size))
            self.pieceName = "w_kn"  

   


class King(Piece):
    def __init__(self,row,column,team,size):
        super().__init__(row,column,team,size)
        
        if team == "black": 
            self.image = pygame.transform.scale(pygame.image.load("Images/b_king.png"), (size,size))
            self.pieceName = "b_ki"
        elif team == "white":
            self.image = pygame.transform.scale(pygame.image.load("Images/w_king.png"), (size,size))
            self.pieceName = "w_ki"          
        
        
   