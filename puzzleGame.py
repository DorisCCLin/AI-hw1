import random
import copy


class puzzleGame:
    up = "up"
    dn = "down"
    lf = "left"
    rg = "right"

    pieceNumber = -1
    xPosition = 0
    yPosition = 0
    height = 1
    width = 1

    def loadGameState():
        state = []
        doc = open('SBP-level0.txt', "r")
        for line in doc:
            field = line.strip().split(",")
            del field[-1]
            state.append(field)

        del state[0]

        for i in range(len(state)):
            for j in range(len(state[i])):
                state[i][j] = int(state[i][j])
        return state

    def displayState(state):
        print(str(len(state[0])) + "," + str(len(state)) + ",")

        for i in range(len(state)):
            print(','.join(map(str, state[i])))

    def cloneState(originalState):
        copiedState = originalState.copy()
        return copiedState

    def completeCheck(state):
        isCompleted = True
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == -1:
                    isCompleted = False
        return isCompleted

    def setPieceSize(state, xPos, yPos, xLimit, yLimit, piece):
        # print("xPos:"+str(xPos)+" yPos"+str(yPos)+" xLimit:"+str(xLimit)+" yLimit:"+str(yLimit))
        width = 0
        height = 0

        for w in range(xPos, xLimit):
            if state[yPos][w] == piece:
                width += 1
            else:
                break

        # set height
        for h in range(yPos, yLimit):
            if state[h][xPos] == piece:
                height += 1
            else:
                break

        return [width, height]

    def availablePieceMoves(state, piece):
        movements = []
        verticalLimit = len(state)
        pieceFound = False
        height = 0
        width = 0

        for i in range(verticalLimit):
            horizontalLimit = len(state[i])
            for j in range(horizontalLimit):
                if state[i][j] == piece:
                    pieceFound = True
                    dimensions = puzzleGame.setPieceSize(
                        state, j, i, horizontalLimit, verticalLimit, piece)
                    width = dimensions[0]
                    height = dimensions[1]
                    if piece == puzzleGame.pieceNumber:
                        puzzleGame.xPosition = j
                        puzzleGame.yPosition = i
                        puzzleGame.width = width
                        puzzleGame.height = height

                    # print("i:"+str(i)+" j:"+str(j)+" piece:"+str(piece)+" width:"+str(width)+" height:"+str(height))
                    # check if piece can move up
                    if state[i-1][j] == 0 or (state[i-1][j] == -1 and state[i][j] == 2):
                        blocked = False
                        if width > 1:
                            for x in range(j+1, horizontalLimit):
                                if state[i][x] == 2 and state[i-1][x] != -1 and state[i-1][x] != 0:
                                    blocked = True
                                elif state[i][x] == piece and state[i][x] != 2 and state[i-1][x] != 0:
                                    blocked = True
                                elif state[i][x] != piece:
                                    break
                        if not blocked:
                            movements.append(puzzleGame.up)
                    # check if piece can move left
                    if state[i][j-1] == 0 or (state[i][j-1] == -1 and state[i][j] == 2):
                        blocked = False
                        if height > 1:
                            for x in range(i+1, verticalLimit):
                                if state[x][j] == 2 and state[x][j-1] != -1 and state[x][j-1] != 0:
                                    blocked = True
                                elif state[x][j] == piece and state[x][j] != 2 and state[x][j-1] != 0:
                                    blocked = True
                                elif state[x][j] != piece:
                                    break
                        if not blocked:
                            movements.append(puzzleGame.lf)
                    # check if piece can move down
                    if state[i+height][j] == 0 or (state[i+height][j] == -1 and state[i][j] == 2):
                        blocked = False
                        if width > 1:
                            for x in range(j+1, horizontalLimit):
                                if state[i+height-1][x] == 2 and state[i+height][x] != -1 and state[i+height][x] != 0:
                                    blocked = True
                                elif state[i+height-1][x] == piece and state[i+height-1][x] != 2 and state[i+height][x] != 0:
                                    blocked = True
                                    break
                                elif state[i+height-1][x] != piece:
                                    break
                        if not blocked:
                            movements.append(puzzleGame.dn)
                    # check if piece can move right
                    if state[i][j+width] == 0 or (state[i][j+width] == -1 and state[i][j] == 2):
                        blocked = False
                        if height > 1:
                            for x in range(i+1, verticalLimit):
                                if state[x][j+width-1] == 2 and state[x][j+width] != -1 and state[x][j+width] != 0:
                                    blocked = True
                                elif state[x][j+width-1] == piece and state[x][j+width-1] != 2 and state[x][j+width] != 0:
                                    blocked = True
                                    break
                                elif state[x][j+width-1] != piece:
                                    break
                        if not blocked:
                            movements.append(puzzleGame.rg)
                    break
            if pieceFound:
                break
        return movements

    def availableBoardMoves(state):
        movements = []
        largestPiece = 0
        for i in range(len(state)):
            if max(state[i]) > largestPiece:
                largestPiece = max(state[i])
        # print(largestPiece)

        for x in range(2, largestPiece + 1):
            if puzzleGame.availablePieceMoves(state, x):
                movements.append((x, puzzleGame.availablePieceMoves(state, x)))
        # print(movements)
        return movements

    # (2,"down") => return new state
    def applyMove(state, move):
        puzzleGame.pieceNumber = move[0]
        availableMoves = puzzleGame.availableBoardMoves(state)
        piece = move[0]
        nextMove = move[1]

        # print("y:"+str(puzzleGame.yPosition)+" x:"+str(puzzleGame.xPosition)+" h:"+str(puzzleGame.height)+" w:"+str(puzzleGame.width))

        for item in availableMoves:
            if item[0] == piece and nextMove in item[1]:
                if nextMove == puzzleGame.up:
                    for y in range(puzzleGame.yPosition-1, puzzleGame.yPosition + puzzleGame.height):
                        for x in range(puzzleGame.xPosition, puzzleGame.xPosition + puzzleGame.width):
                            value = piece
                            if y == puzzleGame.yPosition + puzzleGame.height - 1:
                                value = 0
                            state[y][x] = value
                if nextMove == puzzleGame.dn:
                    for y in range(puzzleGame.yPosition, puzzleGame.yPosition + puzzleGame.height + 1):
                        for x in range(puzzleGame.xPosition, puzzleGame.xPosition + puzzleGame.width):
                            value = piece
                            if y == puzzleGame.yPosition:
                                value = 0
                            state[y][x] = value
                if nextMove == puzzleGame.rg:
                    for y in range(puzzleGame.yPosition, puzzleGame.yPosition + puzzleGame.height):
                        for x in range(puzzleGame.xPosition, puzzleGame.xPosition + puzzleGame.width + 1):
                            value = piece
                            if x == puzzleGame.xPosition:
                                value = 0
                            state[y][x] = value
                if nextMove == puzzleGame.lf:
                    for y in range(puzzleGame.yPosition, puzzleGame.yPosition + puzzleGame.height):
                        for x in range(puzzleGame.xPosition - 1, puzzleGame.xPosition + puzzleGame.width):
                            value = piece
                            if x == puzzleGame.xPosition + puzzleGame.width - 1:
                                value = 0
                            state[y][x] = value

        return state

    def applyMoveCloning(state, move):
        copiedState = state.copy()

        return puzzleGame.applyMove(copiedState, move)

    def stateCompare(state, newState):
        isIdentical = True
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != newState[i][j]:
                    isIdentical = False
        return isIdentical

    def swapIdx(idx1, idx2, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == idx1:
                    state[i][j] = idx2
                elif state[i][j] == idx2:
                    state[i][j] = idx1

    def normalizeState(state):
        nextIdx = 3
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == nextIdx:
                    nextIdx += 1
                elif state[i][j] > nextIdx:
                    puzzleGame.swapIdx(nextIdx, state[i][j], state)
                    nextIdx += 1
        # print(state)
        return state

    def randomWalks(state, number):
        moveCount = 0
        isCompleted = False
        while not isCompleted and moveCount < number:
            print(state)
            puzzleGame.displayState(state)
            # previousState = puzzleGame.cloneState(state)
            availableMoves = puzzleGame.availableBoardMoves(state)
            selectedPiece = random.choice(availableMoves)
            selectedDirection = random.choice(selectedPiece[1])
            selectedMove = (selectedPiece[0], selectedDirection)
            print(selectedMove)
            newState = puzzleGame.applyMoveCloning(state, selectedMove)
            state = puzzleGame.normalizeState(newState)

            if puzzleGame.completeCheck(state):
                isCompleted = True

            moveCount += 1
            print("-------")


# state = puzzleGame.loadGameState()
# print(state)
# puzzleGame.displayState([[1, -1, -1, 1, 1], [1, 0, 3, 4, 1], [1, 0, 2, 2, 1], [1, 1, 1, 1, 1]])
# print (puzzleGame.availablePieceMoves([[1, -1, -1, 1, 1], [1, 2, 2, 4, 1], [1, 0, 0, 3, 1], [1, 1, 1, 1, 1]], 2))
# # puzzleGame.availableBoardMoves(state)
# puzzleGame.displayState([[1, -1, -1, 1, 1], [1, 0, 3, 4, 1], [1, 2, 2, 0, 1], [1, 1, 1, 1, 1]])
# puzzleGame.availableBoardMoves([[1, -1, -1, 1, 1], [1, 0, 3, 4, 1], [1, 2, 2, 0, 1], [1, 1, 1, 1, 1]])
#  ,[ 1  3  0  4  1]
#  ,[ 1  2  2  0  1]
#  .[ 1  1  1  1  1]])
# puzzleGame.displayState(newState)

# print(puzzleGame.completeCheck(state))
# puzzleGame.randomWalks([[1, -1, -1, 1, 1], [1, 0, 5, 8, 1], [1, 0, 2, 2, 1], [1, 1, 1, 1, 1]], 5)
# puzzleGame.displayState(puzzleGame.normalizeState(state))
