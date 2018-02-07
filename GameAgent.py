import copy

def raidpossible(currentboardstate, a, b, player, boardsize):
    p = a - 1
    q = a + 1
    r = b - 1
    s = b + 1
    if p >= 0 and currentboardstate[p][b] == player:
        return True
    if q < boardSize and currentboardstate[q][b] == player:
        return True
    if r >= 0 and currentboardstate[a][r] == player:
        return True
    if s < boardSize and currentboardstate[a][s] == player:
        return True
    return False

def raidneighbor(currentboardstate, a, b, neighbor, player):
    p = a - 1
    q = a + 1
    r = b - 1
    s = b + 1
    if p >= 0 and currentboardstate[p][b] == neighbor:
        currentboardstate[p][b] = player
    if q < boardSize and currentboardstate[q][b] == neighbor:
        currentboardstate[q][b] = player
    if r >= 0 and currentboardstate[a][r] == neighbor:
        currentboardstate[a][r] = player
    if s < boardSize and currentboardstate[a][s] == neighbor:
        currentboardstate[a][s] = player
    return currentboardstate


def minimin(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, queue2):
    myTotal = 0
    opponentTotal = 0
    stakeraid = ''
    tilesleft = 0
    pathtraversed = queue.pop()
    pathtraversed2 = queue2.pop()
    boardState = pathtraversed[-1]
    currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                tilesleft += 1
    if depth == depthlimit or tilesleft == 0:
        for i in range(len(currentboardState)):
            for j in range(len(currentboardState)):
                if currentboardState[i][j] == iam:
                    myTotal += int(cellValues[i][j])
                elif currentboardState[i][j] == opponent:
                    opponentTotal += int(cellValues[i][j])
        gameScore = myTotal - opponentTotal
        return gameScore, currentboardState, pathtraversed, stakeraid, pathtraversed2
    utilityValue = float("Inf")
    boardStateToChose = copy.deepcopy(boardState)
    finalsolpath = copy.deepcopy(pathtraversed)
    solwithraidpath = copy.deepcopy(pathtraversed2)
    #utilityValue = 9999999999999
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                currentboardState[i][j] = opponent
                temppath = list(pathtraversed)
                temppath.append(currentboardState)
                queue.insert(0, temppath)
                temppath2 = list(pathtraversed2)
                temppath2.append(currentboardState)
                queue2.insert(0, temppath2)
                depth += 1
                utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath = minimax(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, queue2)
                if utilityValueReturned < utilityValue:
                    boardStateToChose = boardstateReturned
                    finalsolpath = pathtaken
                    solwithraidpath = raidpath
                    stakeraid = 'Stake'
                utilityValue = min(utilityValue, utilityValueReturned)
                depth -= 1
                currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                raid = raidpossible(currentboardState, i, j, opponent, boardsize)
                if raid == True:
                    currentboardState[i][j] = opponent
                    beforeraidboardstate = copy.deepcopy(currentboardState)
                    currentboardState = raidneighbor(currentboardState, i, j, iam, opponent)
                    temppath = list(pathtraversed)
                    temppath.append(currentboardState)
                    queue.insert(0, temppath)
                    temppath2 = list(pathtraversed2)
                    temppath2.append(beforeraidboardstate)
                    queue2.insert(0, temppath2)
                    depth += 1
                    utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath = minimax(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, queue2)
                    if utilityValueReturned < utilityValue:
                        boardStateToChose = boardstateReturned
                        finalsolpath = pathtaken
                        solwithraidpath = raidpath
                        stakeraid = 'Raid'
                    utilityValue = min(utilityValue, utilityValueReturned)
                    depth -= 1
                    currentboardState = copy.deepcopy(boardState)
    return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath


def minimax(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, queue2):
    myTotal = 0
    opponentTotal = 0
    stakeraid = ''
    tilesleft = 0
    #currentboardState = copy.deepcopy(boardState)
    pathtraversed = queue.pop()
    pathtraversed2 = queue2.pop()
    boardState = pathtraversed[-1]
    currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                tilesleft += 1
    if depth == depthlimit or tilesleft == 0:
        for i in range(len(currentboardState)):
            for j in range(len(currentboardState)):
                if currentboardState[i][j] == iam:
                    myTotal += int(cellValues[i][j])
                elif currentboardState[i][j] == opponent:
                    opponentTotal += int(cellValues[i][j])
        gameScore = myTotal - opponentTotal
        return gameScore, currentboardState, pathtraversed, stakeraid, pathtraversed2
    utilityValue = -float("Inf")
    boardStateToChose = copy.deepcopy(boardState)
    finalsolpath = copy.deepcopy(pathtraversed)
    solwithraidpath = copy.deepcopy(pathtraversed2)
    #utilityValue = -999999999999
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                currentboardState[i][j] = iam
                temppath = list(pathtraversed)
                temppath.append(currentboardState)
                queue.insert(0, temppath)
                temppath2 = list(pathtraversed2)
                temppath2.append(currentboardState)
                queue2.insert(0, temppath2)
                depth += 1
                utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath =  minimin(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, queue2)
                if utilityValueReturned > utilityValue:
                    boardStateToChose = boardstateReturned
                    finalsolpath = pathtaken
                    solwithraidpath = raidpath
                    stakeraid = 'Stake'
                utilityValue = max(utilityValue,utilityValueReturned)
                depth -= 1
                currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                raid = raidpossible(currentboardState, i, j, iam, boardsize)
                if raid == True:
                    currentboardState[i][j] = iam
                    beforeraidboardstate = copy.deepcopy(currentboardState)
                    currentboardState = raidneighbor(currentboardState, i, j, opponent, iam)
                    temppath = list(pathtraversed)
                    temppath.append(currentboardState)
                    queue.insert(0, temppath)
                    temppath2 = list(pathtraversed2)
                    temppath2.append(beforeraidboardstate)
                    queue2.insert(0, temppath2)
                    depth += 1
                    utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath = minimin(cellValues, queue, depthlimit, depth,
                                                                                  iam, opponent, boardsize, queue2)
                    if utilityValueReturned > utilityValue:
                        boardStateToChose = boardstateReturned
                        finalsolpath = pathtaken
                        solwithraidpath = raidpath
                        stakeraid = 'Raid'
                    utilityValue = max(utilityValue, utilityValueReturned)
                    depth -= 1
                    currentboardState = copy.deepcopy(boardState)
    return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath


def alphabetamin(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, alpha, beta, queue2):
    myTotal = 0
    opponentTotal = 0
    stakeraid = ''
    tilesleft = 0
    pathtraversed = queue.pop()
    pathtraversed2 = queue2.pop()
    boardState = pathtraversed[-1]
    currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                tilesleft += 1
    if depth == depthlimit or tilesleft == 0:
        for i in range(len(currentboardState)):
            for j in range(len(currentboardState)):
                if currentboardState[i][j] == iam:
                    myTotal += int(cellValues[i][j])
                elif currentboardState[i][j] == opponent:
                    opponentTotal += int(cellValues[i][j])
        gameScore = myTotal - opponentTotal
        return gameScore, currentboardState, pathtraversed, stakeraid, pathtraversed2
    utilityValue = float("Inf")
    boardStateToChose = copy.deepcopy(boardState)
    finalsolpath = copy.deepcopy(pathtraversed)
    solwithraidpath = copy.deepcopy(pathtraversed2)
    #utilityValue = 9999999999999
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                currentboardState[i][j] = opponent
                temppath = list(pathtraversed)
                temppath.append(currentboardState)
                queue.insert(0, temppath)
                temppath2 = list(pathtraversed2)
                temppath2.append(currentboardState)
                queue2.insert(0, temppath2)
                depth += 1
                utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath = alphabetamax(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, alpha, beta, queue2)
                if utilityValueReturned < utilityValue:
                    boardStateToChose = boardstateReturned
                    finalsolpath = pathtaken
                    solwithraidpath = raidpath
                    stakeraid = 'Stake'
                utilityValue = min(utilityValue, utilityValueReturned)
                if utilityValue <= alpha:
                    return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath
                beta = min(beta, utilityValue)
                depth -= 1
                currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                raid = raidpossible(currentboardState, i, j, opponent, boardsize)
                if raid == True:
                    currentboardState[i][j] = opponent
                    beforeraidboardstate = copy.deepcopy(currentboardState)
                    currentboardState = raidneighbor(currentboardState, i, j, iam, opponent)
                    temppath = list(pathtraversed)
                    temppath.append(currentboardState)
                    queue.insert(0, temppath)
                    temppath2 = list(pathtraversed2)
                    temppath2.append(beforeraidboardstate)
                    queue2.insert(0, temppath2)
                    depth += 1
                    utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath = alphabetamax(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, alpha, beta, queue2)
                    if utilityValueReturned < utilityValue:
                        boardStateToChose = boardstateReturned
                        finalsolpath = pathtaken
                        solwithraidpath = raidpath
                        stakeraid = 'Raid'
                    utilityValue = min(utilityValue, utilityValueReturned)
                    if utilityValue <= alpha:
                        return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath
                    beta = min(beta, utilityValue)
                    depth -= 1
                    currentboardState = copy.deepcopy(boardState)
    return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath




def alphabetamax(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, alpha, beta, queue2):
    myTotal = 0
    opponentTotal = 0
    stakeraid = ''
    tilesleft = 0
    #currentboardState = copy.deepcopy(boardState)
    pathtraversed = queue.pop()
    pathtraversed2 = queue2.pop()
    boardState = pathtraversed[-1]
    currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                tilesleft += 1
    if depth == depthlimit or tilesleft == 0:
        for i in range(len(currentboardState)):
            for j in range(len(currentboardState)):
                if currentboardState[i][j] == iam:
                    myTotal += int(cellValues[i][j])
                elif currentboardState[i][j] == opponent:
                    opponentTotal += int(cellValues[i][j])
        gameScore = myTotal - opponentTotal
        return gameScore, currentboardState, pathtraversed, stakeraid, pathtraversed2
    utilityValue = -float("Inf")
    boardStateToChose = copy.deepcopy(boardState)
    finalsolpath = copy.deepcopy(pathtraversed)
    solwithraidpath = copy.deepcopy(pathtraversed2)
    #utilityValue = -999999999999
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                currentboardState[i][j] = iam
                temppath = list(pathtraversed)
                temppath.append(currentboardState)
                queue.insert(0, temppath)
                temppath2 = list(pathtraversed2)
                temppath2.append(currentboardState)
                queue2.insert(0, temppath2)
                depth += 1
                utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath =  alphabetamin(cellValues, queue, depthlimit, depth, iam, opponent, boardsize, alpha, beta, queue2)
                if utilityValueReturned > utilityValue:
                    boardStateToChose = boardstateReturned
                    finalsolpath = pathtaken
                    solwithraidpath = raidpath
                    stakeraid = 'Stake'
                utilityValue = max(utilityValue,utilityValueReturned)
                if utilityValue >= beta:
                    return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath
                alpha = max(alpha, utilityValue)
                depth -= 1
                currentboardState = copy.deepcopy(boardState)
    for i in range(len(currentboardState)):
        for j in range(len(currentboardState)):
            if currentboardState[i][j] == '.':
                raid = raidpossible(currentboardState, i, j, iam, boardsize)
                if raid == True:
                    currentboardState[i][j] = iam
                    beforeraidboardstate = copy.deepcopy(currentboardState)
                    currentboardState = raidneighbor(currentboardState, i, j, opponent, iam)
                    temppath = list(pathtraversed)
                    temppath.append(currentboardState)
                    queue.insert(0, temppath)
                    temppath2 = list(pathtraversed2)
                    temppath2.append(beforeraidboardstate)
                    queue2.insert(0, temppath2)
                    depth += 1
                    utilityValueReturned, boardstateReturned, pathtaken, strd, raidpath = alphabetamin(cellValues, queue, depthlimit, depth,
                                                                                  iam, opponent, boardsize, alpha, beta, queue2)
                    if utilityValueReturned > utilityValue:
                        boardStateToChose = boardstateReturned
                        finalsolpath = pathtaken
                        solwithraidpath = raidpath
                        stakeraid = 'Raid'
                    utilityValue = max(utilityValue, utilityValueReturned)
                    if utilityValue >= beta:
                        return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath
                    alpha = max(alpha, utilityValue)
                    depth -= 1
                    currentboardState = copy.deepcopy(boardState)
    return utilityValue, boardStateToChose, finalsolpath, stakeraid, solwithraidpath





def calculate(a,b):
    temp = []
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i][j] != b[i][j]:
                temp.append([i,j])
                return temp




with open('input.txt', 'r') as f:
    file = f.read()
    mainList = file.splitlines()

boardSize = int(mainList[0])
algo = mainList[1]
player = mainList[2]
depthlimit = int(mainList[3])

cellValues = []
for i in mainList[4:4 + int(boardSize)]:
    j = i.split(" ")
    cellValues.append(j)

boardState = []
for i in mainList[3 + (int(boardSize) + 1) : ]:
    j = list(i)
    boardState.append(j)

if player == 'X':
    iam = 'X'
    opponent = 'O'
else:
    iam = 'O'
    opponent = 'X'

xTotal = 0
oTotal = 0
depth = 0
alpha = -float("Inf")
beta = float("Inf")

queue = [[boardState]]
queue2 = [[boardState]]
path = [boardState]

if algo == 'MINIMAX':
    score, boardStateSelect, pathtaken, stakeorraid, raidpathtaken = minimax(cellValues, queue, depthlimit, depth, iam, opponent, boardSize, queue2)
else:
    score, boardStateSelect, pathtaken, stakeorraid, raidpathtaken = alphabetamax(cellValues, queue, depthlimit, depth, iam, opponent, boardSize, alpha, beta, queue2)


nextmoveworaid = raidpathtaken[1]
nextmove = pathtaken[1]

rowcolumn = calculate(boardState, nextmoveworaid)

number = rowcolumn[0][0]
letter = rowcolumn[0][1]

rowvalue = number + 1
columnletter = chr(letter + ord('A'))

with open('output.txt', 'w') as fwrite:
    fwrite.write(columnletter + '' + str(rowvalue) + ' ' + stakeorraid + '\n')
    for i in nextmove:
        for j in i:
            fwrite.write(j)
        fwrite.write('\n')
