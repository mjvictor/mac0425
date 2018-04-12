# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node:
    def __init__(self, father, successor):
        self.state = successor[0]
        self.action = successor[1]
        self.cost = successor[2]
        self.father = father


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""
    flag = True
    visited = []
    ret = []
    
    stack = util.Stack()
    currentState = [problem.getStartState(), None, None]
    currentState = Node(None, currentState)

    visited.append(currentState)
    
    while not problem.isGoalState(currentState.state) and flag:

        for successor in problem.getSuccessors(currentState.state):
            newNode = Node(currentState, successor)
            stack.push(newNode)

        
        if not stack.isEmpty():
            explored = True
            while not stack.isEmpty() and explored:
                explored = False
                currentState = stack.pop()
                for item in visited:
                    if currentState.state == item.state:
                        explored = True
                        break
            if not explored:
                visited.append(currentState)

            else:
                flag = False
        else :
            flag = False

    #print path
    if problem.isGoalState(currentState.state):
        tmpStack = util.Stack()
        searchNode = currentState
        while searchNode.father != None:
            tmpStack.push(searchNode)
            searchNode = searchNode.father

        while not tmpStack.isEmpty():
            aux = tmpStack.pop()
            ret.append(aux.action)
    
    else: 
        print "Impossivel"

    return ret
   
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = []
    ret = []
    
    currentState = [problem.getStartState(), None, None]
    currentState = Node(None,currentState)
    visited.append(currentState)

    #popState
    flag = True

    while not problem.isGoalState(currentState.state) and flag:
        for successor in problem.getSuccessors(currentState.state):
            newNode = Node(currentState, successor)
            queue.push(newNode)
        
        if not queue.isEmpty():
            explored = True
            while not queue.isEmpty() and explored:
                explored = False
                currentState = queue.pop()
                for item in visited:
                    if item.state == currentState.state:
                        explored = True
                        break
            
            if not explored:
                visited.append(currentState)
            else:
                flag = False
        else :
            flag = False

    tmpStack = util.Stack()
    
    if problem.isGoalState(currentState.state):
        searchNode = currentState 
        while searchNode.father != None:
            tmpStack.push(searchNode)
            searchNode = searchNode.father

        while not tmpStack.isEmpty():
            aux = tmpStack.pop()
            ret.append(aux.action)
            
    else :
        print "Eh impossivel"

    return ret 
    
    
    #util.raiseNotDefined()

class InterativeNode:

    def __init__(self, father, successor, height):
        self.father = father
        self.state = successor[0]
        self.action = successor[1]
        self.cost = successor[2]
        self.h = height
        

def iterativeDeepeningSearch(problem):
    """
    Start with depth = 0.
    Search the deepest nodes in the search tree first up to a given depth.
    If solution not found, increment depth limit and start over.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    "*** YOUR CODE HERE ***"
    ret = []
    stack = util.Stack()
    visited = []

    startState = [problem.getStartState(), None, None]
    startNode = InterativeNode(None, startState, 0) 

    depth = 0
        
    currentNode = startNode
    visited.append(currentNode)
    flag = False

    while not flag:
        flag = True
        visited = []
    	while not problem.isGoalState(currentNode.state) and flag:
   	    if currentNode.h < depth:
   	        for successor in problem.getSuccessors(currentNode.state):
   	            newNode = InterativeNode(currentNode, successor,currentNode.h + 1)
   	            stack.push(newNode)

   	    if not stack.isEmpty():
   	        explored = True
                while not stack.isEmpty() and explored:
                    explored = False
                    currentNode = stack.pop()
                    for item in visited:
                        if currentNode.state == item.state and item.h <= currentNode.h + 1:
                                explored = True
                                break
                
                if not explored:
                    visited.append(currentNode)
   	        else :
                    flag = False
            else:
   	        flag = False

        if not flag:
            depth += 1
            currentNode = startNode

    if problem.isGoalState(currentNode.state):
        tmpStack = util.Stack()
        searchNode = currentNode
        while searchNode.father != None:
            tmpStack.push(searchNode)
            searchNode = searchNode.father

        while not tmpStack.isEmpty():
            aux = tmpStack.pop()
            ret.append(aux.action)

    else:
        print "Impossivel"

    return ret

    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

class aStarNode:

    def __init__(self, father, successor, f, g):
        self.father = father
        self.state = successor[0]
        self.action = successor[1]
        self.cost = successor[2]
        self.f = f
        self.g = g


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    ret = []
    visited = []
    flag = True
    minPq = util.PriorityQueueWithFunction(lambda x: x.f)
    
    startNode = [problem.getStartState(), None, None]
    startNode = aStarNode(None, startNode, heuristic(startNode[0], problem), 0)

    currentNode = startNode
    visited.append(currentNode)

    while not problem.isGoalState(currentNode.state) and flag:
        for successor in problem.getSuccessors(currentNode.state):
            newG = currentNode.g + successor[2]
            newF = heuristic(successor[0], problem) + newG
            newNode = aStarNode(currentNode, successor, newF, newG)
            minPq.push(newNode)
        
        if not minPq.isEmpty():
            explored = True
            while not minPq.isEmpty() and explored:
                explored = False
                currentNode = minPq.pop()
                for item in visited:
                    if currentNode.state == item.state and item.f <= currentNode.f:
                            explored = True
                            break
            if not explored:
                visited.append(currentNode)
            else :
                flag = False
        else:
            flag = False

    if problem.isGoalState(currentNode.state):
        tmpStack = util.Stack()
        searchNode = currentNode
        while searchNode.father != None:
            tmpStack.push(searchNode)
            searchNode = searchNode.father

        while not tmpStack.isEmpty():
            aux = tmpStack.pop()
            ret.append(aux.action)
    else:
        print "Impossivel"

    return ret


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
