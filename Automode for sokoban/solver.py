import sys
import collections
import numpy as np
import heapq
import math
import time
import numpy as np
global posWalls, posGoals


"""Load puzzles and define the rules of sokoban"""

def transferToGameState(layout):
    """Transfer the layout of initial puzzle"""
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]

    maxColsNum = max([len(x) for x in layout])

    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ': layout[irow][icol] = 0   # free space
            elif layout[irow][icol] == '#': layout[irow][icol] = 1 # wall
            elif layout[irow][icol] == '&': layout[irow][icol] = 2 # player
            elif layout[irow][icol] == 'B': layout[irow][icol] = 3 # box
            elif layout[irow][icol] == '.': layout[irow][icol] = 4 # goal
            elif layout[irow][icol] == 'X': layout[irow][icol] = 5 # box on goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 

    # print(layout)
    return np.array(layout)
def transferToGameState2(layout, player_pos):
    """Transfer the layout of initial puzzle"""
    maxColsNum = max([len(x) for x in layout])
    temp = np.ones((len(layout), maxColsNum))
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            temp[i][j] = layout[i][j]

    temp[player_pos[1]][player_pos[0]] = 2
    return temp

def PosOfPlayer(gameState):
    """Return the position of agent"""
    return tuple(np.argwhere(gameState == 2)[0]) # e.g. (2, 2)

def PosOfBoxes(gameState):
    """Return the positions of boxes"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5))) # e.g. ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5))

def PosOfWalls(gameState):
    """Return the positions of walls"""
    return tuple(tuple(x) for x in np.argwhere(gameState == 1)) # e.g. like those above

def PosOfGoals(gameState):
    """Return the positions of goals"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5))) # e.g. like those above

def isEndState(posBox):
    """Check if all boxes are on the goals (i.e. pass the game)"""
    return sorted(posBox) == sorted(posGoals)

def isLegalAction(action, posPlayer, posBox):
    """Check if the given action is legal"""
    xPlayer, yPlayer = posPlayer

    if action[-1].isupper(): # the move was a push
        x1, y1 = xPlayer + 2 * action[0], yPlayer + 2 * action[1]
    else:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
    return (x1, y1) not in posBox + posWalls

def legalActions(posPlayer, posBox):
    """Return all legal actions for the agent in the current game state"""
    allActions = [[-1,0,'u','U'],[1,0,'d','D'],[0,-1,'l','L'],[0,1,'r','R']]

    xPlayer, yPlayer = posPlayer
    legalActions = []

    for action in allActions:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]

        if (x1, y1) in posBox: # the move was a push
            action.pop(2) # drop the little letter

        else:
            action.pop(3) # drop the upper letter

        if isLegalAction(action, posPlayer, posBox):
            legalActions.append(action)

        else: 
            continue     
    
    return tuple(tuple(x) for x in legalActions) # e.g. ((0, -1, 'l'), (0, 1, 'R'))

def updateState(posPlayer, posBox, action):
    """Return updated game state after an action is taken"""
    xPlayer, yPlayer = posPlayer # the previous position of player

    newPosPlayer = [xPlayer + action[0], yPlayer + action[1]] # the current position of player
    
    posBox = [list(x) for x in posBox]
   
    if action[-1].isupper(): # if pushing, update the position of box
        posBox.remove(newPosPlayer)
        posBox.append([xPlayer + 2 * action[0], yPlayer + 2 * action[1]])
    
    posBox = tuple(tuple(x) for x in posBox)
    newPosPlayer = tuple(newPosPlayer)
    
    return newPosPlayer, posBox

def isFailed(posBox):
    """This function used to observe if the state is potentially failed, then prune the search"""
    rotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
    flipPattern = [[2,1,0,5,4,3,8,7,6],
                    [0,3,6,1,4,7,2,5,8],
                    [2,1,0,5,4,3,8,7,6][::-1],
                    [0,3,6,1,4,7,2,5,8][::-1]]
    allPattern = rotatePattern + flipPattern

    for box in posBox:
        if box not in posGoals:
            board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                    (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
            for pattern in allPattern:
                newBoard = [board[i] for i in pattern]
                if newBoard[1] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posBox and newBoard[2] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posBox and newBoard[2] in posWalls and newBoard[5] in posBox: return True
                elif newBoard[1] in posBox and newBoard[2] in posBox and newBoard[5] in posBox: return True
                elif newBoard[1] in posBox and newBoard[6] in posBox and newBoard[2] in posWalls and newBoard[3] in posWalls and newBoard[8] in posWalls: return True
    return False

#DFS algorithm
#The details explanation for some general line I put on the UCS part
def depthFirstSearch(gameState):
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)

    startState = (beginPlayer, beginBox)
    frontier = collections.deque([[startState]])
    exploredSet = set()
    actions = [[0]] 
    temp = []

    while frontier:
        node = frontier.pop()
        node_action = actions.pop()
    
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break
    
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
    
            for action in legalActions(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)
    
                if isFailed(newPosBox):
                    continue
    
                frontier.append(node + [(newPosPlayer, newPosBox)])
                actions.append(node_action + [action[-1]])
    
    return temp


#BFS algorithm
def breadthFirstSearch(gameState):
    #initialize algorithm
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)

    startState = (beginPlayer, beginBox) # e.g. ((2, 2), ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5)))
    
    #use queue type, I used deque then take actions with the leftmost elements in the deque but not the rightmost
    frontier = collections.deque([[startState]]) # store states
    actions = collections.deque([[0]]) # store actions
    exploredSet = set()
    temp = []

    #while the queue still exists
    while frontier:
        #the difference between dfs code and bfs code is that:
        #dfs use deque.pop(), which means pop the rightmost elements due to the stack's concept
        #bfs use deque.popleft(), which means pop the leftmost elements due to the queue's concept
        node = frontier.popleft() 
        node_action = actions.popleft()

        #check whether the algorithm is ended sucessfully
        #then return the actions series 
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break 
        
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
        
            for action in legalActions(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)
        
                if isFailed(newPosBox):
                    continue
        
                frontier.append(node + [(newPosPlayer, newPosBox)])
                actions.append(node_action + [action[-1]])
    return temp
    

#Uniform Cost Search Algorithm 
class PriorityQueue:
    #a priorityy queue using the heap method
    def  __init__(self):
        self.Heap = []
        self.Count = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap)
        return item

    def isEmpty(self):
        return len(self.Heap) == 0

#cost function
def get_cost(actions):
    #change cost function into calculate each step as minus one point
    return actions.count('l') + actions.count('r') + actions.count('u') + actions.count('d')

def uniformCostSearch(gameState):
    #initialize environment and variables
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)

    #create a Priority Queue to take the minumum cost from action space
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], 0)
    
    cost = 0
    temp = []
    
    while frontier: #while still exists the action in the queue
        node = frontier.pop()       #take the state node out of the queue 
        node_action = actions.pop() #take a legal action from action space

        #if the game is finished, save the whole process to the temp list and exit from the loop
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break

        #if the graph is yet visited
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            #choose one legal actions to try
            for action in legalActions(node[-1][0], node[-1][1]):
                #update new position after choose action
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)

                #if the algorithm is terminated then back to loop
                if isFailed(newPosBox):
                    continue

                #or else
                #put the new state node into the queue
                frontier.push(node + [(newPosPlayer, newPosBox)], get_cost(action))
                #put the action node into the priority queue and take the cost as the priority number
                actions.push(node_action + [action[-1]], get_cost(action))
    return temp

#Greedy search
gamma = .7
def greedyNaive(gameState):
    temp = []
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)

    #create a Priority Queue to take the minumum cost from action space
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], 0)
    
    cost = 0
    
    while frontier: #while still exists the action in the queue
        cnt = 0
        node = frontier.pop()       #take the state node out of the queue 
        node_action = actions.pop() #take a legal action from action space

        #if the game is finished, save the whole process to the temp list and exit from the loop
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break

        #if the graph is yet visited
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            #choose one legal actions to try    
            for action in legalActions(node[-1][0], node[-1][1]):
                cnt += 1
                #update new position after choose action
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)

                #if the algorithm is terminated then back to loop
                if isFailed(newPosBox):
                    continue

                #or else
                #put the new state node into the queue
                frontier.push(node + [(newPosPlayer, newPosBox)], get_cost(action)*gamma)
                #put the action node into the priority queue and take the cost as the priority number
                actions.push(node_action + [action[-1]], get_cost(action)*gamma) 
    return temp 

#Euclidean greedy search
#the function to estimate the euclidean distance from the boxes to the goals
def euclideanDist(gameState):
    distance = 0
    box_position = PosOfBoxes(gameState)
    goal_position = PosOfGoals(gameState)
    for i in range(len(box_position)):
        distance += math.sqrt((goal_position[i][0] - box_position[i][0])**2 + (goal_position[i][1] - box_position[i][1])**2)
    return distance

def greedy_euclidean(gameState):
    temp = []
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)

    #create a Priority Queue to take the minumum cost from action space
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], 0)
    
    cost = 0
    
    while frontier: #while still exists the action in the queue
        cnt = 0
        node = frontier.pop()       #take the state node out of the queue 
        node_action = actions.pop() #take a legal action from action space

        #if the game is finished, save the whole process to the temp list and exit from the loop
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break

        #if the graph is yet visited
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            #choose one legal actions to try    
            for action in legalActions(node[-1][0], node[-1][1]):
                cnt += 1
                #update new position after choose action
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)

                #if the algorithm is terminated then back to loop
                if isFailed(newPosBox):
                    continue

                #or else
                #put the new state node into the queue
                frontier.push(node + [(newPosPlayer, newPosBox)], euclideanDist(gameState))
                #put the action node into the priority queue and take the Euclidean distance as the priority number
                actions.push(node_action + [action[-1]], euclideanDist(gameState))
    return temp

#Mahattan greedy
#This function is to estimate the Mahattan distance between the boxes and goals
def mahattan_distance(gameState):
    distance = 0
    box_position = PosOfBoxes(gameState)
    goal_position = PosOfGoals(gameState)
    for i in range(len(box_position)):
        distance += abs(goal_position[i][0] - box_position[i][0]) + abs(goal_position[i][1] - box_position[i][1])
    return distance

def greedy_mahattan(gameState):
    temp = []
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)

    #create a Priority Queue to take the minumum cost from action space
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], 0)
    
    cost = 0
    
    while frontier: #while still exists the action in the queue
        cnt = 0
        node = frontier.pop()       #take the state node out of the queue 
        node_action = actions.pop() #take a legal action from action space

        #if the game is finished, save the whole process to the temp list and exit from the loop
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break

        #if the graph is yet visited
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            #choose one legal actions to try    
            for action in legalActions(node[-1][0], node[-1][1]):
                cnt += 1
                #update new position after choose action
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)

                #if the algorithm is terminated then back to loop
                if isFailed(newPosBox):
                    continue

                #or else
                #put the new state node into the queue
                frontier.push(node + [(newPosPlayer, newPosBox)], mahattan_distance(gameState))
                #put the action node into the priority queue and take the Mahattan distance as the priority number
                actions.push(node_action + [action[-1]], mahattan_distance(gameState))
    return temp

#The combination from 3 different greedy strategies above
def greedy_combination(gameState):
    temp = []
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)

    #create a Priority Queue to take the minumum cost from action space
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], 0)
    
    cost = 0
    
    while frontier: #while still exists the action in the queue
        cnt = 0
        node = frontier.pop()       #take the state node out of the queue 
        node_action = actions.pop() #take a legal action from action space

        #if the game is finished, save the whole process to the temp list and exit from the loop
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break

        #if the graph is yet visited
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            #choose one legal actions to try    
            for action in legalActions(node[-1][0], node[-1][1]):
                cnt += 1
                #update new position after choose action
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)

                #if the algorithm is terminated then back to loop
                if isFailed(newPosBox):
                    continue

                #or else
                #put the new state node into the queue
                frontier.push(node + [(newPosPlayer, newPosBox)], (mahattan_distance(gameState) + euclideanDist(gameState)) *gamma)
                #put the action node into the priority queue
                #take the Mahattan and Euclidean distance with a discounted factor gamma as the priority number
                actions.push(node_action + [action[-1]], (mahattan_distance(gameState) + euclideanDist(gameState))*gamma)
    return temp

#A* search
def a_star(gameState):
    temp = []
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)

    #create a Priority Queue to take the minumum cost from action space
    frontier = PriorityQueue()
    frontier.push([startState], 0)
    
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], 0)
    
    cost = 0
    
    while frontier: #while still exists the action in the queue
        cnt = 0
        node = frontier.pop()       #take the state node out of the queue 
        node_action = actions.pop() #take a legal action from action space

        #if the game is finished, save the whole process to the temp list and exit from the loop
        if isEndState(node[-1][-1]):
            temp += node_action[1:]
            break

        #if the graph is yet visited
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])

            #choose one legal actions to try    
            for action in legalActions(node[-1][0], node[-1][1]):
                cnt += 1
                #update new position after choose action
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)

                #if the algorithm is terminated then back to loop
                if isFailed(newPosBox):
                    continue

                #or else
                #put the new state node into the queue
                frontier.push(node + [(newPosPlayer, newPosBox)], euclideanDist(gameState) + get_cost(action))
                #put the action node into the priority queue and take the Euclidean distance and cost function from UCS as the priority number
                actions.push(node_action + [action[-1]], euclideanDist(gameState) + get_cost(action))
    return temp


def readCommand(argv):
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option('-l', '--level', dest='sokobanLevels',
                      help='level of game to play', default='level1.txt')
    parser.add_option('-m', '--method', dest='agentMethod',
                      help='research method', default='bfs')
    args = dict()
    options, _ = parser.parse_args(argv)
    with open('assets/levels/' + options.sokobanLevels,"r") as f: 
        layout = f.readlines()
    args['layout'] = layout
    args['method'] = options.agentMethod
    return args

def get_move(layout, player_pos, method):
    time_start = time.time()
    global posWalls, posGoals
    gameState = transferToGameState2(layout, player_pos)
    posWalls = PosOfWalls(gameState)
    posGoals = PosOfGoals(gameState)
    if method == 'dfs':
        result = depthFirstSearch(gameState)
    elif method == 'bfs':
        result = breadthFirstSearch(gameState)    
    elif method == 'ucs':
        result = uniformCostSearch(gameState)
    elif method == 'greedy':
        result = greedy(gameState)
    elif method == 'a_star':
        result = a_star(gameState)
    elif method == 'greedy-euclidean':
        result = greedy_euclidean(gameState)
    elif method == 'greedy-mahattan':
        result = greedy_mahattan(gameState)
    elif method == 'greedy-comb':
        result = greedy_combination(gameState)
    else:
        raise ValueError('Invalid method.')
    time_end=time.time()
    print('Runtime of %s: %.2f second.' %(method, time_end-time_start))
    print(result)
    return result
