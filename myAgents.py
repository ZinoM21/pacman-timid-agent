
from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent
from util import manhattanDistance
import math


class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """

    def __init__(self):
        super().__init__()  # Call parent constructor
        self.leftTurnAgent = LeftTurnAgent()  # Instantiate LeftTurnAgent

    def inDanger(self, pacman, ghost, dist=3):
        """inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger we return the direction to the ghost.
        """

        # return early if ghost is scared (no danger then) -> avoids manhattanDistance() call
        if ghost.isScared(): 
            return Directions.STOP

        pacmanPos = pacman.getPosition()
        ghostPos = ghost.getPosition()
        sameColumn = pacmanPos[0] == ghostPos[0]
        sameRow = pacmanPos[1] == ghostPos[1]

        # check if in range & same row / column, and return direction to ghost
        if manhattanDistance(pacmanPos, ghostPos) <= dist:
            if sameColumn:
                if pacmanPos[1] < ghostPos[1]:
                    return Directions.NORTH
                else:
                    return Directions.SOUTH
            elif sameRow:
                if pacmanPos[0] < ghostPos[0]:
                    return Directions.EAST
                else:
                    return Directions.WEST
               
            
        # no danger
        return Directions.STOP
    
    def getAction(self, state):
        """
        Make a decision based on the current game state:
        If pacman is in danger, returns direction away from ghost (escape danger)
        If pacman is not in danger, behaves like LeftTurnAgent
        
        state - GameState
        
        returns a valid action direction: North, East, South, West or
        a Stop action when no legal actions are possible
        """

        pacman = state.getPacmanState()
        ghosts = state.getGhostStates()
        legal = state.getLegalPacmanActions()

        for ghost in ghosts:
            directionOfDanger = self.inDanger(pacman, ghost)
            if directionOfDanger != Directions.STOP:
                # in Danger! -> Escape danger

                reverse = Directions.REVERSE[directionOfDanger]
                left = Directions.LEFT[directionOfDanger]
                right = Directions.RIGHT[directionOfDanger]

                if reverse in legal:
                    return reverse
                elif left in legal:
                    return left
                elif right in legal:
                    return right
                elif directionOfDanger in legal:
                    return directionOfDanger
                else:
                    return Directions.STOP
            

        # No danger -> behave like LeftTurnAgent
        return self.leftTurnAgent.getAction(state)