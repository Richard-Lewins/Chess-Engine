import pygame

class OptionBox():

    def __init__(self, x, y, w, h, color, highlightColor, font, optionList, selected = 0):
        self.color = color
        self.highlight_color = highlightColor
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.optionList = optionList
        self.selected = selected
        self.drawMenu = False
        self.menuActive = False
        self.activeOption = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menuActive else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.optionList[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.drawMenu:
            for i, text in enumerate(self.optionList):
                #If drawmenu is true, for each of the items in the textbox
                rect = self.rect.copy() #Create a new rectangle for the new box
                rect.y += (i+1) * self.rect.height  #The new y coordinate is just below the previous box
                pygame.draw.rect(surf, self.highlight_color if i == self.activeOption else self.color, rect)#Draw the new box
                msg = self.font.render(text, 1, (0, 0, 0)) #Write the message
                surf.blit(msg, msg.get_rect(center = rect.center))
            #This is for the black box around
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.optionList))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        #IF the mouse is hovered over, set self.menuActive to true
        self.menuActive = self.rect.collidepoint(mpos)
        
        self.activeOption = -1
        for i in range(len(self.optionList)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos): #If the button is hovered over a certain optiton, set this to the active option
                self.activeOption = i
                break

        if not self.menuActive and self.activeOption == -1:
            self.drawMenu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #If the button is clicked, and the entire menu is drawn
                #Set the new selected option to be the option that is hovered over
                if self.menuActive:
                    self.drawMenu = not self.drawMenu
                elif self.drawMenu and self.activeOption >= 0:
                    self.selected = self.activeOption
                    self.drawMenu = False
                    return self.activeOption
        return -1


class button():
    def __init__(self, x, y, w, h, color, highlightColor, font,text,callBackFunction):
        self.color = color
        self.highlightColor = highlightColor
        self.rect = pygame.Rect(x, y, w, h)
        self.hovered = False
        self.text = text
        self.font = font
        self.callbackFunction = callBackFunction
        

    def draw(self, surf):
        #Draw the button. If the mouse is hovering over the button, draw it as highlightColor
        pygame.draw.rect(surf, self.highlightColor if self.hovered else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.text, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

    #This functino gets called each "tick" of the whileloop
    def update(self,eventList):
        mpos = pygame.mouse.get_pos()
        #If the mouse is hovered over, set self.hovered to TRUE
        self.hovered = self.rect.collidepoint(mpos)

        for event in eventList:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    #If the mouse is over the button, and the button is clicked, call the callback fucntion
                    self.callbackFunction()

