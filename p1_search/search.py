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
from typing import Set, Any

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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    """
    2 data structures
    explored - set of explored nodes
    fringe - stack of possible nodes to expand next
        - tuple of current game state and set of past actions
    """
    #initailize explored set and fringe, push start state to fringe and explored set
    explored = set()
    fringe = util.Stack()
    fringe.push((problem.getStartState(), []))
    explored.add(problem.getStartState())


    while fringe.isEmpty() == False:
        current_state, actions = fringe.pop()
        # check for goal state, if met return list of actions
        if problem.isGoalState(current_state):
            return actions
        explored.add(current_state)
        #expand and push successors to fringe
        for n in problem.getSuccessors(current_state):
            new_state = n[0]
            new_action = n[1]
            #push new state to fringe
            if new_state not in explored:
                fringe.push((new_state, actions + [new_action]))


    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """
        2 data structures
        explored - set of explored nodes
        fringe - queue of possible nodes to expand next
            - tuple of current game state and set of past actions
        """
    # initailize explored list and fringe, push start state to fringe and explored list
    explored = []
    fringe = util.Queue()
    fringe.push((problem.getStartState(), []))
    explored += [problem.getStartState()]

    while fringe.isEmpty() == False:
        current_state, actions = fringe.pop()
        # check for goal state, if met return list of actions
        if problem.isGoalState(current_state):
            return actions

        for n in problem.getSuccessors(current_state):
            new_state = n[0]
            new_action = n[1]
            # add current state to explored and push new state to fringe
            if new_state not in explored:
                fringe.push((new_state, actions + [new_action]))
                explored += [new_state]
    return []
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """
           2 data structures
           explored - set of explored nodes
           fringe - priority queue of possible nodes to expand next
               - tuple of current game state, set of past actions and cost of current path
           """
    # initailize explored set and fringe, push start state to fringe
    explored = set()
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)

    while fringe.isEmpty() == False:
        current_state, actions, cost = fringe.pop()
        # check for goal state, if met return list of actions
        if problem.isGoalState(current_state):
            return actions
        # add current state to explored
        if current_state not in explored:
            explored.add(current_state)
            #expand and push succssors to fringe
            for n in problem.getSuccessors(current_state):
                new_state = n[0]
                new_action = n[1]
                new_cost = n[2] + cost
                fringe.push((new_state, actions + [new_action], new_cost), new_cost)

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
              2 data structures
              explored - set of explored nodes
              fringe - priority queue of possible nodes to expand next
                  - tuple of current game state, set of past actions and cost of current path
              """
    # initailize explored set and fringe, push start state to fringe
    explored = []
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))

    while fringe.isEmpty() == False:
        current_state, actions, cost = fringe.pop()
        # check for goal state, if met return list of actions
        if problem.isGoalState(current_state):
            return actions
        #add current state to explored
        if current_state not in explored:
            explored.append(current_state)

            for n in problem.getSuccessors(current_state):
                new_state = n[0]
                new_action = n[1]
                new_cost = n[2] + cost
                fringe.push((new_state, actions + [new_action], new_cost), new_cost + heuristic(new_state, problem))

    util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
