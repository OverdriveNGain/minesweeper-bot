from math import e
import funcs
import time

print("2 second init...")
time.sleep(2)
while True:
    funcs.reset()
    funcs.clickMiddle()
    board = None
    mines = funcs.getMineCount()
    for i in range(9999):
        print(f"Cycle {i}")

        board= funcs.getValues(board)

        actioned, mines = funcs.markObvious(board, mines)

        if (mines == 0):
            break

        if actioned:
            continue

        subtractedBoard = funcs.getSubtractedBoard(board)
        actioned, mines = funcs.mark12(board, mines, subtractedBoard)

        if actioned:
            continue
        break
        
    if (mines == 0):
        break
print("Done!")