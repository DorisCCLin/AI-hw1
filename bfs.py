import puzzleGame
import copy

# visited = []
# queue = []

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

visited = []  # List to keep track of visited nodes.
queue = []  # Initialize a queue


def bfs(visited, state):
    # visited.append(node)
    # queue.append(node)
    normalizedState = puzzleGame.puzzleGame.normalizeState(state)
    visited.append(normalizedState)
    possibleMoves = puzzleGame.puzzleGame.availableBoardMoves(normalizedState)
    puzzleGame.puzzleGame.displayState(normalizedState)
    copiedState = copy.deepcopy(normalizedState)
    puzzleGame.puzzleGame.displayState(copiedState)
    if possibleMoves:
        currentQueue = []
        for pair in possibleMoves:
            for direction in pair[1]:
                currentQueue.append((pair[0], direction))
        queue.append(currentQueue)
        # print(queue)
        # print(queue[-1][0])
        puzzleGame.puzzleGame.displayState(normalizedState)

        newState = puzzleGame.puzzleGame.applyMoveCloning(
            normalizedState, queue[-1][0])

        puzzleGame.puzzleGame.displayState(normalizedState)

        # newNormalizedState = puzzleGame.puzzleGame.normalizeState(newState)
        # if newNormalizedState not in visited:
        #     visited.append(newNormalizedState)

        # print(puzzleGame.puzzleGame.stateCompare(
        #     newState, prevState))
        puzzleGame.puzzleGame.displayState(normalizedState)
        puzzleGame.puzzleGame.displayState(copiedState)
        print(id(normalizedState))
        print(id(copiedState))
        print(visited)
    else:
        newState = puzzleGame.puzzleGame.applyMoveCloning(
            normalizedState, queue)

    # while queue:
    #     s = queue.pop(0)
    #     print(s, end=" ")

    #     for neighbour in graph[s]:
    #         if neighbour not in visited:
    #             visited.append(neighbour)
    #             queue.append(neighbour)


# Driver Code
bfs(visited, puzzleGame.puzzleGame.loadGameState())
