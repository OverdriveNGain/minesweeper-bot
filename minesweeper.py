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
        # funcs.printBoard(board)
        # input("Press enter to proceed with marking obvious")
        # time.sleep(1)
        actioned, mines = funcs.markObvious(board, mines)
        # funcs.printBoard(board)
        # input("Press enter to proceed with next cycle")
        # time.sleep(1)

        # print(f"-----------------------------------------{i}")
        # print(f"Cycle {i} done")
        if (mines == 0):
            break

        if actioned:
            continue
        
    if (mines == 0):
        break
    break
print("Done!")