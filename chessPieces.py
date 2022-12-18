import pygame

class Piece:
    def __init__(self,row,column,team,size,image):
        self.boardPosition = [row,column]
        self.screenPosition = [column*size,row*size]
        self.team = team
        self.imageName = image
        self.pieceName = image[:4]
        self.image = pygame.transform.scale(pygame.image.load("Images/"+image), (size,size))

    def getMoves(self,pieces):
        return []


class Pawn(Piece):
    def __init__(self,row,column,team,size,image):
        super().__init__(row,column,team,size,image)



class Queen(Piece):
    def __init__(self,row,column,team,size,image):
        super().__init__(row,column,team,size,image)
    


class Rook(Piece):
    def __init__(self,row,column,team,size,image):
        super().__init__(row,column,team,size,image)


class Bishop(Piece):
    def __init__(self,row,column,team,size,image):
        super().__init__(row,column,team,size,image)

   

class Knight(Piece):
    def __init__(self,row,column,team,size,image):
        super().__init__(row,column,team,size,image)

   


class King(Piece):
    def __init__(self,row,column,team,size,image):
        super().__init__(row,column,team,size,image)
        self.inCheck = False
        
   