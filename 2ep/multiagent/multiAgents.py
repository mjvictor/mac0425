# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        """scores = []
        pacmanActions = gameState.getLegalActions(0)
        for action in pacmanActions:
            nextGameState = gameState.generateSuccessor(0, action)
            scores.append(self.minGhosts(nextGameState, 1))
        bestAction = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestAction]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        
        return pacmanActions[ chosenIndex]"""
        action = self.maxValue(gameState, 1)    
        return action

    def minGhosts(self, gameState, ghostStates, i):
        if i >= gameState.getNumAgents():
            ghostStates.append(gameState)
            return ghostStates

        v = float('inf')
        currentActions = gameState.getLegalActions(i)
        if currentActions == []:
            ghostStates = self.minGhosts(gameState, ghostStates, i + 1)
            return ghostStates

        for action in currentActions:
            ghostStates = self.minGhosts(gameState.generateSuccessor(i, action), ghostStates, i + 1)

        return ghostStates

    def minValue(self, gameState, depth):

        ghostStates = self.minGhosts(gameState, [], 1)
        if ghostStates == []:
            return self.evaluationFuncion(gameState)
            
        v = float('inf')
        if depth == self.depth:
            for state in ghostStates:
                nextGameState = state
                v = min(v, self.evaluationFunction(nextGameState))
        else :
            for state in ghostStates:
                nextGameState = state
                v = min(v, self.maxValue(nextGameState, depth + 1))
                
        return v

    def maxValue(self, gameState, depth):
        actions = gameState.getLegalActions(0) 
        if actions == []:
            return self.evaluationFunction(gameState)

        bestAction = actions[0]
        v = -float('inf')
        for action in actions:
            nextGameState = gameState.generateSuccessor(0, action)
            tmp = v
            minValue = self.minValue(nextGameState, depth)
            v = max(v, minValue)
            if v != tmp:
                bestAction = action
        if depth == 1:
            return bestAction
        return v
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        plusInf = float('inf')
        minusInf = -plusInf
        action = self.maxValue(gameState, 1, plusInf, minusInf)
        return action

    def maxValue(self, gameState, depth, alfa, beta):
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(gameState)
        
        bestAction = actions[0]
        v = -float('inf')
        for action in actions:
            nextGameState = gameState.generateSuccessor(0, action)
            tmp = v
            minValue = self.minValue(nextGameState, depth, alfa, beta)
            v = max(v, minValue)
            if v != tmp:
                bestAction = action
            if v > beta:
                if depth == 1:
                    return bestAction
                return v
            alfa = max(alfa, v)
        if depth == 1:
            return bestAction
        return v

    def minValue(self, gameState, depth, alfa, beta):
        ghostStates = self.minGhosts(gameState, [], 1, alfa, beta)
        if ghostStates == []:
            return self.evaluationFunction(gameState)
       
        v = float('inf')
        if depth == self.depth:
            for state in ghostStates:
                nextGameState = state
                maxValue = self.evaluationFunction(nextGameState)
                v = min(v, maxValue)
                if v < alfa:
                    return v
                beta = min(beta, v)
        else:
            for state in ghostStates:
                nextGameState = state
                maxValue = self.maxValue(nextGameState, depth + 1, alfa, beta)
                v = min(v, maxValue)
                if v < alfa:
                    return v
                beta = min(beta,v)
        return v
    
    def minGhosts(self, gameState, ghostStates, i, alfa, beta):
        if i >= gameState.getNumAgents():
            ghostStates.append(gameState)
            return ghostStates

        actions = gameState.getLegalActions(i)
        if actions == []:
            ghostStates = self.minGhosts(gameState, ghostStates, i+1, alfa, beta)
            return ghostStates
        
        v = float('inf')

        for action in actions:
            nextGameState = gameState.generateSuccessor(i, action)
            ghostStates = self.minGhosts(nextGameState, ghostStates, i + 1, alfa, beta)

        return ghostStates

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 1)

    def maxValue(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if actions == []:
            return self.evaluationFunction(gameState)
        bestAction = actions[0]
        v = -float('inf')
        for action in actions:
            nextGameState = gameState.generateSuccessor(0, action)
            tmp = v
            expect = self.expectValue(nextGameState, depth)
            tmp = v
            v = max(v, expect)
            if v != tmp:
                bestAction = action
        if depth == 1:
            return bestAction
        return v

    def expectGhosts(self, gameState, ghostStates, i):
        if i >= gameState.getNumAgents():
            ghostStates.append(gameState)
            return ghostStates
        
        actions = gameState.getLegalActions(i)
        if actions == []:
            ghostStates = self.expectGhosts(gameState, ghostStates, i+1)
            return ghostStates
        
        for action in actions:
            nextGameState = gameState.generateSuccessor(i, action)
            ghostStates = self.expectGhosts(nextGameState, ghostStates, i + 1)
        return ghostStates

    def expectValue(self, gameState, depth):
        ghostStates = self.expectGhosts(gameState, [], 1)
        if ghostStates == []:
            return self.evaluationFunction(gameState)

        v = 0
        p = 1.0/float(len(ghostStates))
        if depth == self.depth:
            for state in ghostStates:
                actionValue = self.evaluationFunction(state)
                v += p * actionValue
        else :
            for state in ghostStates:
                actionValue = self.maxValue(state, depth + 1)
                v += p * actionValue
        return v

        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

