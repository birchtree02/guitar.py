import pygame
import sys
from colours import *

# sizes
WIDTH = 250
HEIGHT = 250
BUFFER = 10
FONT_SIZE = 30
CIRCLE_FONT_SIZE = 15

# other values
STRINGS = 6
FRETS  = 5


class GuitarDisplay():
    def __init__(self, guitar, chord=None):
        pygame.init()
        pygame.display.set_caption('guitar')

        self.guitar = guitar

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface.fill(BG_COLOUR)

        self.initialiseValues()
        self.drawGrid()

        self.setString(string=0, fret=2, number=2) # test code to display a G chord
        self.setString(string=1, fret=1, number=1)
        self.setString(string=2, fret=0, number=0)
        self.setString(string=3, fret=0, number=0)
        self.setString(string=4, fret=0, number=0)
        self.setString(string=5, fret=2, number=3)


        pygame.display.update()

        self.waitForClose()

    def initialiseValues(self):    
        self.stringsStartBufferY = BUFFER+FONT_SIZE*2 # to make space for string labels
        self.stringSize = HEIGHT-(self.stringsStartBufferY + BUFFER)
    
    def drawGrid(self):
        for i in range(STRINGS): # vertical
            stringX = BUFFER + (self.stringSize//(STRINGS-1))*i

            self.drawText(self.guitar.getStringNotes()[i], (stringX-FONT_SIZE//4, BUFFER))
            pygame.draw.line(self.surface, LINE_COLOUR, (stringX, 0+self.stringsStartBufferY), (stringX, self.stringsStartBufferY+self.stringSize))

        for i in range(FRETS+1): # horizontal
            lineY = self.stringsStartBufferY + (self.stringSize//(FRETS))*i
            pygame.draw.line(self.surface, LINE_COLOUR, (0+BUFFER, lineY), (0+BUFFER+self.stringSize, lineY))

    def setString(self, string, fret, number):
        number = {-1:"x",0:"o",1:"\u2776",2:"\u2777",3:"\u2778"}[number]
        labelX = BUFFER + (self.stringSize//(STRINGS-1))*string - CIRCLE_FONT_SIZE//2
        labelY = self.stringsStartBufferY + fret*self.stringSize//FRETS - CIRCLE_FONT_SIZE//2 - (self.stringSize//FRETS)//2
        self.drawText(str(number), (labelX, labelY))


    def drawText(self, text, position):
        font = pygame.font.Font(pygame.font.match_font("calibri"), CIRCLE_FONT_SIZE) if ord(text) > 128 else pygame.font.Font(None, FONT_SIZE)
        text = font.render(text, True, TEXT_COLOUR, BG_COLOUR)
        self.surface.blit(text, position)

    def waitForClose(self):
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break

class Guitar():
    def __init__(self):
        self.stringNotes = ["E", "A", "D", "G", "B", "E"]

    def getStringNotes(self):
        return self.stringNotes


GuitarDisplay(Guitar())