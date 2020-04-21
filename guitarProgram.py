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

# music
NOTE_NUMBERS = {"A":0,"A#":1,"Bb":1,"B":2,"C":3,"C#":4,"Db":4,"D":5,"D#":6,"Eb":6,"E":7,"F":8,"F#":9,"Gb":9,"G":10,"G#":11,"Ab":11}
DEFAULT_TUNING = ["E", "A", "D", "G", "B", "E"]

class GuitarDisplay():
    def __init__(self, guitar, highlights=None):
        pygame.init()
        pygame.display.set_caption('guitar')

        self.guitar = guitar

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface.fill(BG_COLOUR)

        self.initialiseValues()
        self.drawGrid()

        if highlights: self.highlightFrets(highlights)

        self.waitForClose()

        pygame.display.quit()


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

    def highlightFrets(self, highlights):
        for i, highlight in enumerate(highlights):
            self.setString(i, highlight[0], highlight[1])

    def setString(self, string, fret, number):
        #number = {-1:"x",0:"o",1:"\u2776",2:"\u2777",3:"\u2778"}[number]
        number = {-1:"x",0:"o",1:"1",2:"2",3:"3",4:"4",5:"5"}[number]
        labelX = BUFFER + (self.stringSize//(STRINGS-1))*string - CIRCLE_FONT_SIZE//2
        labelY = self.stringsStartBufferY + fret*self.stringSize//FRETS - CIRCLE_FONT_SIZE//2 - (self.stringSize//FRETS)//2
        self.drawText(str(number), (labelX, labelY))


    def drawText(self, text, position):
        font = pygame.font.Font(pygame.font.match_font("Calibri"), CIRCLE_FONT_SIZE) if ord(text) > 128 else pygame.font.Font(None, FONT_SIZE)
        text = font.render(text, True, TEXT_COLOUR, BG_COLOUR)
        self.surface.blit(text, position)

    def waitForClose(self):
        while True:
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break

class Guitar():
    def __init__(self, notes=DEFAULT_TUNING):
        self.stringNotes = notes
        self.strings = [String(note) for note in self.stringNotes]

    def getStringNotes(self):
        return self.stringNotes

    def display(self, chord=None): # todo: make it display how a particular chord is played on the guitar
        GuitarDisplay(self, self.getChordPositions(chord) if chord else None)

    def getChordPositions(self, chord):
        # todo: determine what number should be applied to each fret
        # todo: make sure that each note of the chord is chosen
        chord = getChord(chord)
        print(f'chord={chord}')
        unchosenNotes = chord[:] # copy list
        fretNumbers = []
        fretLabels = []
        for i, string in enumerate(self.strings):
            notePositions = [string.notePosition(chord[0])] if chord==unchosenNotes else [string.notePosition(note) for note in chord]
            minPosition = min(notePositions)
            if minPosition > 3:
                fretNumbers.append(-1)
            else:
                chosenNote = chord[notePositions.index(minPosition)]
                fretNumbers.append(minPosition)
                if chosenNote in unchosenNotes:
                    unchosenNotes.remove(chosenNote) # removes the chosen note from unchosenNotes


        while unchosenNotes:
            print(f'unchosenNotes={unchosenNotes}')
            if [0] in fretNumbers:
                pass
            else:
                pass
        fretLabels = [None, None, None, None, None, None]
        for i, fret in enumerate(fretNumbers): # assign a label to the frets
            if fret < 1:
                fretLabels[i] = fret
                fretNumbers[i] = 0
        currentFinger = 1
        rowNumber = 1
        while None in fretLabels: 
            #Assign fingerings 
            for i, fret in enumerate(fretNumbers):
                if fret == rowNumber:
                    fretLabels[i] = currentFinger
                    currentFinger += 1
            rowNumber += 1


        fretDetails = []
        for i in range(STRINGS):
            fretDetails.append([fretNumbers[i], fretLabels[i]])

        return fretDetails


class String():
    def __init__(self, note="E"):
        self.tune(note)

    def tune(self, note):
        self.note = note
        self.noteNumber = NOTE_NUMBERS[note]

    def notePosition(self, note):
        note = NOTE_NUMBERS[note]
        if note < self.noteNumber:
            note += 12
        return note-self.noteNumber

def getChord(chordString="G"): # todo: make it return the notes of the given chord programmatically
    pass

def getChord(chordString="G"): # hardcoded solution for the getChord function
    return {
        "G":["G","B","D"], 
        "A":["A","C#","E"], 
        "D":["D","F#","A"], 
        "E":["E","G#","B"], 
        "C":["C","E","G"], 
        "Emin":["E","G","B"]
            }[chordString]

# GuitarDisplay(Guitar(), [[0,-1],[0,0],[2,1],[2,1],[2,1],[0,0]])
Guitar().display("A")