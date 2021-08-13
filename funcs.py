import pyautogui as oto
from pyscreeze import showRegionOnScreen
import constants as const
import math

def clickAtCell(x, y, modifier = 'left'):
    cellSize = const.cellWidth
    oto.click(
        const.boardMinPoint[0] + cellSize * 0.5 + cellSize * x,
        const.boardMinPoint[1] + cellSize * 0.5 + cellSize * y, button= modifier)

def clickMiddle():
    clickAtCell(math.floor(const.boardWidth / 2), math.floor(const.boardHeight / 2))

def getMineCount():
    return const.mineCount

def getValues(lastBoard):
    board = lastBoard
    if board == None:
        print("Generating new board...")
        board = [[-10 for y in range(const.boardHeight)]for x in range(const.boardWidth)]

    region = (
        const.boardMinPoint[0],
        const.boardMinPoint[1],
        const.boardMaxPoint[0],
        const.boardMaxPoint[1],
    )
    regionScreenshot = oto.screenshot(region=(region))
    for y in range(const.boardHeight):
        for x in range(const.boardWidth):
            if (board[x][y] < 0):
    # for y in range(6):
    #     for x in range(6):
                board[x][y] = inspect(regionScreenshot, x, y)

    return board

def inspect(screenshot, x, y):
    pixelXOrigin = const.cellWidth * x
    pixelYOrigin = const.cellHeight * y
    pixelX = pixelXOrigin + const.cellClosed[0]
    pixelY = pixelYOrigin + const.cellClosed[1]
    if const.sameColor(screenshot.getpixel((pixelX, pixelY)), const.cellClosed[2]):
        return -10
    # get number scores
    scores = [0 for i in range(9)]
    pixelY = pixelYOrigin + const.cellTestingPadding
    pixelXMax = pixelXOrigin + const.cellWidth + const.cellTestingPadding - const.cellTestingPadding
    pixelYMax = pixelYOrigin + const.cellHeight + const.cellTestingPadding - const.cellTestingPadding
    while (pixelY < pixelYMax):
        pixelX = pixelXOrigin + const.cellTestingPadding
        while (pixelX < pixelXMax):
            pixel = screenshot.getpixel((pixelX, pixelY))
            if const.sameColor(pixel, const.boardColors):
                scores[0] += 1
            for scoreIndex in range(1, 9):
                if const.sameColor(pixel, const.numberColors[scoreIndex - 1]):
                    scores[scoreIndex] += 1
            pixelX += 4
        pixelY += 4
    max = scores[1]
    maxI = 1
    for i in range(2, len(scores)):
        if (scores[i] > max):
            max = scores[i]
            maxI = i
    if (max == 0):
        return 0
    return -maxI

def printBoard(board):
    for y in range(const.boardHeight):
        lineToPrint = ""
        for x in range(const.boardWidth):
            val = board[x][y]
            if val == -10:
                lineToPrint += "    "
            else:
                lineToPrint += str(board[x][y]).rjust(4, " ")
        print(lineToPrint)

def markObvious(board, mines):
    actioned = False
    for y in range(const.boardHeight):
        for x in range(const.boardWidth):
            val = -board[x][y]
            if (1 <= val <= 8):
                unknown = 0
                flags = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if (0 <= x + dx < const.boardWidth and 0 <= y + dy < const.boardHeight):
                            dval = board[x + dx][y + dy]
                            if (dval == -10):
                                unknown += 1
                            if (dval == 12):
                                flags += 1
                # print(f"                       ({x},{y}):({unknown},{flags},{val})")
                if (flags + unknown == val):
                    # print(f"Mark1 at ({x},{y})")
                    actioned = True
                    board[x][y] = val
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if (0 <= x + dx < const.boardWidth and 0 <= y + dy < const.boardHeight):
                                dval = board[x + dx][y + dy]
                                if (dval == -10):
                                    clickAtCell(x + dx, y + dy, 'right')
                                    board[x + dx][y + dy] = 12
                                    mines -= 1
                                    print(f"Marking mine at ({x + dx},{y + dy}). {mines} mine(s) left")
                elif (val == flags and unknown > 0):
                    # print(f"Mark2 at ({x},{y})")
                    actioned = True
                    board[x][y] = val
                    clickAtCell(x, y, 'middle')
                    # for dx in range(-1, 2):
                    #     for dy in range(-1, 2):
                    #         if (0 <= x + dx < const.boardWidth and 0 <= y + dy < const.boardHeight):
                    #             dval = board[x + dx][y + dy]
                    #             if (dval == -10):
                    #                 clickAtCell(x + dx, y + dy)
                    #                 board[x+dx][y+dy] = -11     
    return (actioned, mines)
                                
def reset():
    oto.leftClick(const.resetButtonAt[0], const.resetButtonAt[1])