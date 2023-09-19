import pygame, sys, time
from pygame.locals import *
from random import *
from math import floor

pygame.init()
surface = pygame.display.set_mode((400, 500), 0, 32)
pygame.display.set_caption("Programming Competition for Computer Club")

gamefont = pygame.font.SysFont("OwnGame/Noto_Kufi_Arabic/NotoKufiArabic-VariableFont_wght.ttf", 40)
scorefont = pygame.font.SysFont("OwnGame/Noto_Kufi_Arabic/NotoKufiArabic-VariableFont_wght.ttf", 30)
sizeofboard = 4  # Define the size of the board here
totalpoints = 0

tileofmatrix = [
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0]
               ]
undomat = []

white = pygame.Color('white')
blue = pygame.Color('blue')
gray = pygame.Color('gray')
darkgray = pygame.Color("darkgray")
yellow = pygame.Color("yellow")
orange = pygame.Color("orange")
lightblue = pygame.Color("lightblue")
deeppurple = (103, 58, 183)
pink = (234, 30, 99)
purple = (156, 39, 176)
deeporange = (255, 87, 34)
red = (255, 0, 0)
brown = (121, 85, 72)
darkblue = pygame.Color('darkblue')
thecolordictionary = {
    0: white,
    2: blue,
    4: darkblue,
    8: yellow,
    16: pink,
    32: purple,
    64: deeppurple,
    128: orange,
    256: deeporange,
    512: darkgray,
    1024: brown,
    2048: red
}


def getcolor(i):
    return thecolordictionary[i]


# Starting with the main function
def mainfunction(fromLoaded=False):
    global sizeofboard  
    global totalpoints  

    if not fromLoaded:
        placerandomtile()
        placerandomtile()
    printmatrix()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if checkIfCanGo() == True:
                if event.type == KEYDOWN:
                    if isArrow(event.key):
                        rotations = getrotations(event.key)
                        addToUndo()
                        for i in range(0, rotations):
                            rotatematrixclockwise()

                        if canmove():
                            movetiles()
                            mergetiles()
                            placerandomtile()

                        for j in range(0, (4 - rotations) % 4):
                            rotatematrixclockwise()

                        printmatrix()
            else:  # just checking wait
                gameover()

            if event.type == KEYDOWN:
                global sizeofboard

                if event.key == pygame.K_r:
                    reset()
                if 50 < event.key < 56:
                    sizeofboard = event.key - 48
                    reset()
                if event.key == pygame.K_s:
                    savegame()
                elif event.key == pygame.K_l:
                    loadgame()
                elif event.key == pygame.K_u:
                    undo()

        pygame.display.update()


def canmove():
    for i in range(0, sizeofboard):
        for j in range(1, sizeofboard):
            if tileofmatrix[i][j - 1] == 0 and tileofmatrix[i][j] > 0:
                return True
            elif (tileofmatrix[i][j - 1] == tileofmatrix[i][j]) and tileofmatrix[i][j - 1] != 0:
                return True
    return False


# This module moves
def movetiles():
    for i in range(0, sizeofboard):
        for j in range(0, sizeofboard - 1):

            while tileofmatrix[i][j] == 0 and sum(tileofmatrix[i][j:]) > 0:
                for k in range(j, sizeofboard - 1):
                    tileofmatrix[i][k] = tileofmatrix[i][k + 1]
                tileofmatrix[i][sizeofboard - 1] = 0


def mergetiles():
    global totalpoints

    for i in range(0, sizeofboard):
        for k in range(0, sizeofboard - 1):
            if tileofmatrix[i][k] == tileofmatrix[i][k + 1] and tileofmatrix[i][k] != 0:
                tileofmatrix[i][k] = tileofmatrix[i][k] * 2
                tileofmatrix[i][k + 1] = 0
                totalpoints += tileofmatrix[i][k]
                movetiles()


def placerandomtile():
    c = 0
    for i in range(0, sizeofboard):
        for j in range(0, sizeofboard):
            if tileofmatrix[i][j] == 0:
                c += 1

    k = floor(random() * sizeofboard * sizeofboard)
    print("click")

    while tileofmatrix[floor(k / sizeofboard)][k % sizeofboard] != 0:
        k = floor(random() * sizeofboard * sizeofboard)

    tileofmatrix[floor(k / sizeofboard)][k % sizeofboard] = 2


def floor(n):
    return int(n - (n % 1))


def printmatrix():
    surface.fill(color=white)
    global sizeofboard
    global totalpoints

    for i in range(0, sizeofboard):
        for j in range(0, sizeofboard):
            pygame.draw.rect(surface, getcolor(tileofmatrix[i][j]),
                             (i * (400 / sizeofboard), j * (400 / sizeofboard) + 100, 400 / sizeofboard, 400 / sizeofboard))
            label = gamefont.render(str(tileofmatrix[i][j]), 1, (255, 255, 255))
            label2 = scorefont.render("YourScore:" + str(totalpoints), 1, (255, 255, 255))
            surface.blit(label, (i * (400 / sizeofboard) + 30, j * (400 / sizeofboard) + 130))
            surface.blit(label2, (10, 20))


def checkIfCanGo():
    for i in range(0, sizeofboard ** 2):
        if tileofmatrix[floor(i / sizeofboard)][i % sizeofboard] == 0:
            return True

    for i in range(0, sizeofboard):
        for j in range(0, sizeofboard - 1):
            if tileofmatrix[i][j] == tileofmatrix[i][j + 1]:
                return True
            elif tileofmatrix[j][i] == tileofmatrix[j + 1][i]:
                return True
    return False


def convertToLinearMatrix():
    mat = []
    for i in range(0, sizeofboard ** 2):
        mat.append(tileofmatrix[floor(i / sizeofboard)][i % sizeofboard])

    mat.append(totalpoints)
    return mat


def addToUndo():
    undomat.append(convertToLinearMatrix())


def rotatematrixclockwise():
    for i in range(0, int(sizeofboard / 2)):
        for k in range(i, sizeofboard - i - 1):
            temp1 = tileofmatrix[i][k]
            temp2 = tileofmatrix[sizeofboard - 1 - k][i]
            temp3 = tileofmatrix[sizeofboard - 1 - i][sizeofboard - 1 - k]
            temp4 = tileofmatrix[k][sizeofboard - 1 - i]

            tileofmatrix[sizeofboard - 1 - k][i] = temp1
            tileofmatrix[sizeofboard - 1 - i][sizeofboard - 1 - k] = temp2
            tileofmatrix[k][sizeofboard - 1 - i] = temp3
            tileofmatrix[i][k] = temp4


def gameover():
    global totalpoints

    surface.fill(color=white)

    label = gamefont.render("gameover", 1, (255, 255, 255))
    label2 = gamefont.render("score : " + str(totalpoints), 1, (255, 255, 255))
    label3 = gamefont.render("press 'R' to play again", 1, (255, 255, 255))

    surface.blit(label, (50, 100))
    surface.blit(label2, (50, 200))
    surface.blit(label3, (50, 300))


def reset():
    global totalpoints
    global tileofmatrix

    totalpoints = 0
    surface.fill(color=white)
    tileofmatrix = [[0 for i in range(0, sizeofboard)] for j in range(0, sizeofboard)]
    mainfunction()


def savegame():
    f = open("savedata", "w")

    line1 = " ".join([str(tileofmatrix[floor(x / sizeofboard)][x % sizeofboard]) for x in range(0, sizeofboard ** 2)])
    f.write(line1 + "\n")
    f.write(str(sizeofboard) + "\n")
    f.write(str(totalpoints))
    f.close


def undo():
    if len(undomat) > 0:
        mat = undomat.pop()

        for i in range(0, sizeofboard ** 2):
            tileofmatrix[floor(i / sizeofboard)][i % sizeofboard] = mat[i]
        global totalpoints
        totalpoints = mat[sizeofboard ** 2]

        printmatrix()


def loadgame():
    global totalpoints
    global sizeofboard
    global tilematrix

    f = open("savedata", "r")

    mat = (f.readline()).split(' ', sizeofboard ** 2)
    sizeofboard = int(f.readline())
    totalpoints = int(f.readline())

    for i in range(0, sizeofboard ** 2):
        tileofmatrix[floor(i / sizeofboard)][i % sizeofboard] = int(mat[i])

    f.close()


def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)


def getrotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT :
        return 1
    elif k == pygame.K_RIGHT :
        return 3


mainfunction()

pygame.quit()
