# boardWidth = 18
# boardHeight = 14
# boardMinPoint = [0,146]
# boardMaxPoint = [675,671]

# https://minesweeperonline.com/
boardMinPoint = (89,161)
boardMaxPoint = (569,417)
boardFirstCell = (105, 177)
resetButtonAt = (330, 136)
mineCount = 99
boardColors = (189, 189, 189)
cellClosed = (1, 1, (255, 255, 255)) # cell position plus (1, 1) has color (255, 255 ,5225)
cellTestingPadding = 3
colorDifferenceThreshold = 20
numberColors = [
    (0, 0, 255),
    (1, 127, 1),
    (255, 0, 0),
    (0, 0, 128),
    (129, 1, 2),
    (0, 128, 128),
    (0, 0, 0),
    (128, 128, 128),
]

boardPixelWidth = boardMaxPoint[0] - boardMinPoint[0]
boardPixelHeight = boardMaxPoint[1] - boardMinPoint[1]
boardWidth = round(boardPixelWidth / (boardFirstCell[0] - boardMinPoint[0]))
boardHeight = round(boardPixelHeight / (boardFirstCell[1] - boardMinPoint[1]))
cellWidth = boardPixelWidth / boardWidth
cellHeight = boardPixelHeight / boardHeight
testingCellWidth = cellWidth - cellTestingPadding * 2
testingCellHeight = cellHeight - cellTestingPadding * 2

def sameColor(c1,c2):
    return (
        abs(c1[0] - c2[0]) < colorDifferenceThreshold and
        abs(c1[1] - c2[1]) < colorDifferenceThreshold and
        abs(c1[2] - c2[2]) < colorDifferenceThreshold)