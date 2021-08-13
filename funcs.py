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
                                
def getSubtractedBoard(board):
    subtractedBoard = [[0 for y in range(len(board[x]))] for x in range(len(board))]
    for y in range(const.boardHeight):
        for x in range(const.boardWidth):
            val = board[x][y]
            if (val == 12):
                subtractedBoard[x][y] = 0
            elif (-8 <= val <= -1):
                for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if (0 <= x + dx < const.boardWidth and 0 <= y + dy < const.boardHeight):
                                dval = board[x + dx][y + dy]
                                if (dval == 12):
                                    val += 1
                subtractedBoard[x][y] = val
            elif (val == -10):
                subtractedBoard[x][y] = -10
    return subtractedBoard

def mark12(board, mines, subtractedBoard):
    actioned = False

    def flag(x, y, board, mines):
        clickAtCell(x, y, 'right')
        board[x][y] = 12
        mines -= 1
        print(f"Marking mine at ({x},{y}) with 1-2 strategy. {mines} mine(s) left")
        return (board, mines)

    def evalLast3(
        x, # x post of -2
        y, # y pos of -2
        board,
        subtractedBoard,
        mines,
        dir, # "north", "south", "east", "west" -> direction to go to -1
        nEdge, # if -2 cell is at north edge
        sEdge, # if -2 cell is at south edge
        wEdge, # if -2 cell is at west edge
        eEdge):  # if -2 cell is at east edge

        positions = []
        if (dir == "north"):
            if (not sEdge):
                positions += [(x,y + 1)]
                if (not wEdge):
                    positions += [(x - 1, y + 1)]
                if (not eEdge):
                    positions += [(x + 1, y + 1)]
        elif (dir == "south"):
            if (not nEdge):
                positions += [(x,y - 1)]
                if (not wEdge):
                    positions += [(x - 1, y - 1)]
                if (not eEdge):
                    positions += [(x + 1, y - 1)]
        elif (dir == "east"):
            if (not wEdge):
                positions += [(x - 1,y)]
                if (not nEdge):
                    positions += [(x - 1, y - 1)]
                if (not sEdge):
                    positions += [(x - 1, y + 1)]
        elif (dir == "west"):
            if (not eEdge):
                positions += [(x + 1,y)]
                if (not nEdge):
                    positions += [(x + 1, y - 1)]
                if (not sEdge):
                    positions += [(x + 1, y + 1)]
        unFilteredDebugPositions = positions
        positions = [position for position in positions if subtractedBoard[position[0]][position[1]] == -10]
        if (len(positions) == 1 and board[positions[0][0]][positions[0][1]] != 12):
            m = flag(positions[0][0], positions[0][1], board, mines)
            # print("------------------------")
            # print(x)
            # print(y)
            # print(mines)
            # print(dir)
            # print(nEdge)
            # print(sEdge)
            # print(wEdge)
            # print(eEdge)
            # print(positions)
            # print(unFilteredDebugPositions)
            return (True, m[0], m[1])
        return (False, board,mines)

    for y in range(const.boardHeight):
        for x in range(const.boardWidth):
            val = subtractedBoard[x][y]
            if (val == -2):
                nEdge = y == 0
                sEdge = y == const.boardHeight - 1
                wEdge = x == 0
                eEdge = x == const.boardWidth - 1
                actionedOnThisCell = False

                # check 1 in north
                if (not nEdge):
                    northval = subtractedBoard[x][y - 1]
                    if (northval == -1):
                        actionedOnThisCell, board, mines = evalLast3(x, y, board, subtractedBoard, mines, "north", nEdge, sEdge, wEdge, eEdge)
                # check 1 in south
                if (not sEdge):
                    southval = subtractedBoard[x][y + 1]
                    if (southval == -1):
                        actionedOnThisCell, board, mines = evalLast3(x, y, board, subtractedBoard, mines, "south", nEdge, sEdge, wEdge, eEdge)
                # check 1 in east
                if (not eEdge):
                    eastval = subtractedBoard[x + 1][y]
                    if (eastval == -1):
                        actionedOnThisCell, board, mines = evalLast3(x, y, board, subtractedBoard, mines, "east", nEdge, sEdge, wEdge, eEdge)
                # check 1 in west
                if (not wEdge):
                    westval = subtractedBoard[x - 1][y]
                    if (westval == -1):
                        actionedOnThisCell, board, mines = evalLast3(x, y, board, subtractedBoard, mines, "west", nEdge, sEdge, wEdge, eEdge)
                
                if (actionedOnThisCell):
                    actioned = True
    return (actioned, mines)
  

def reset():
    oto.leftClick(const.resetButtonAt[0], const.resetButtonAt[1])