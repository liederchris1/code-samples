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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        "distance to furthest food pellet"
        food = newFood.asList()
        min_Food_Dist = -1

        for f in food:
            d_food = manhattanDistance(newPos, f)
            if d_food < min_Food_Dist or min_Food_Dist == -1:
                min_Food_Dist = d_food

        "distance to ghosts"

        ghost_Dist = 0

        for g in newGhostStates:
            g_pos = g.getPosition()
            d = manhattanDistance(newPos, g_pos)
            ghost_Dist += d
            if ghost_Dist == 0:
                ghost_Dist = .1

        return successorGameState.getScore() + (1/float(min_Food_Dist)*4 - (1/float(ghost_Dist)))


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

    # max for pacman (true), min for ghosts(false)

    def Minimax(self, depth, agentIndex, gameState):

        # checks of the game is over or at the end of the tree
        if gameState.isWin() or gameState.isLose() or self.depth < depth:
            return self.evaluationFunction(gameState)
        # make a list of all the possible actions so you can select the max and min later on 
        actions = gameState.getLegalActions(agentIndex)
        actionList = []
        for a in actions:
            successor = gameState.generateSuccessor(agentIndex, a)
            # if this is the last agent at this depth, move to the next level
            # if not explore the next agent at this depth
            if (agentIndex + 1) >= gameState.getNumAgents():
                actionList += [self.Minimax(depth + 1, 0, successor)]
            else:
                actionList += [self.Minimax(depth, agentIndex + 1, successor)]
        # if agent is pacman return max action
        # this is essentially the max-value and min-value functions
        if agentIndex == 0 and depth == 1:
            max1 = max(actionList)
            length = len(actionList)
            for i in range(length):
                if actionList[i] == max1:
                    return actions[i]

        if agentIndex == 0 and depth !=1:
            returnAction = max(actionList)
        # if agent is ghost return min action
        if agentIndex > 0:
            returnAction = min(actionList)
        return returnAction

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        return self.Minimax(1, 0, gameState)

        # return return_action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def AlphaBeta(self, depth, agentIndex, a, b, gameState):
        alpha = a
        beta = b

        # checks of the game is over or at the end of the tree
        if gameState.isWin() or gameState.isLose() or self.depth < depth:
            return self.evaluationFunction(gameState)

        # make a list of all the possible actions so you can select the max and min later on
        actions = gameState.getLegalActions(agentIndex)
        actionList = []
        for x in actions:
            successor = gameState.generateSuccessor(agentIndex, x)
            # if this is the last agent at this depth, move to the next level
            # if not explore the next agent at this depth
            if (agentIndex + 1) >= gameState.getNumAgents():
                act = self.AlphaBeta(depth + 1, 0, alpha, beta, successor)
            else:
                act = self.AlphaBeta(depth, agentIndex + 1, alpha, beta, successor)

            # the following 3 if statements perform the alpha beta pruning as outlined in the slides
            if (agentIndex == 0 and act > beta) or (agentIndex > 0 and act < alpha):
                return act
            if agentIndex == 0 and act > alpha:
                alpha = act
            if agentIndex > 0 and act < beta:
                beta = act

            actionList += [act]

        # if agent is pacman return max action
        if agentIndex == 0 and depth == 1:
            max_score = max(actionList)
            length = len(actionList)
            for i in range(length):
                if actionList[i] == max_score:
                    return actions[i]

        if agentIndex == 0 and depth != 1:
            returnA = max(actionList)
        # if agent is ghost return min action
        if agentIndex > 0:
            returnA = min(actionList)
        return returnA

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(1, 0, -10000000, 100000000, gameState)
        util.raiseNotDefined()

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
        util.raiseNotDefined()

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
