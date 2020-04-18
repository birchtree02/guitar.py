import pygame
from colours import *

# sizes
WIDTH = 250
HEIGHT = 250
BUFFER = 10
FONT_SIZE = 30

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

        self.drawGrid()

        pygame.display.update()

        self.waitForClose()
        
    def drawGrid(self):
        stringsStartBufferY = BUFFER+FONT_SIZE*2 # to allow for string labels
        # stringsStartBufferY = BUFFER
        stringSize = HEIGHT-(stringsStartBufferY + BUFFER)

        for i in range(STRINGS): # vertical
            stringX = BUFFER + (stringSize//(STRINGS-1))*(i)

            self.drawText(self.guitar.getStringNotes()[i], (stringX-FONT_SIZE//4, BUFFER))
            pygame.draw.line(self.surface, LINE_COLOUR, (stringX, 0+stringsStartBufferY), (stringX, stringsStartBufferY+stringSize))

        for i in range(FRETS+1): # horizontal
            lineY = stringsStartBufferY + (stringSize//(FRETS))*i
            pygame.draw.line(self.surface, LINE_COLOUR, (0+BUFFER, lineY), (0+BUFFER+stringSize, lineY))


    def drawText(self, text, position):
        text_surface = pygame.font.Font(None, FONT_SIZE)
        text = text_surface.render(text, True, TEXT_COLOUR)
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