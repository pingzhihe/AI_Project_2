# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction
from .game_class import Game
from .mcts import monte_carlo_tree_search, take_action
from .boardupdate import spawnaction_convertor, \
    spreadaction_convertor,spread_convertor,spawn_convertor
from .minmax import mx_find_best_move
#from .alpla_beta_tb import ab_find_best_move
from .alpha_beta import ab_find_best_move
from .alpha_beta_2 import ab_find_best_move_2

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        #The activate code: python -m referee agent agent
        """
        Initialise the agent.
        """

        self.game = Game()
        self._color = color
        self.transposition_table = {}
        match color:
            case PlayerColor.RED:
                self.game.player = 'r'
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                self.game.player = 'b'
                print("Testing: I am playing as blue")


        


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """ 

        match self._color:
            case PlayerColor.RED:
                self.game.player = 'r'
                action = ab_find_best_move_2(self.game)
                if len(action) == 2:
                    return spawnaction_convertor(action)
                else:
                    return spreadaction_convertor(action)
                
                
            case PlayerColor.BLUE:
                self.game.player = 'b'
                action = ab_find_best_move(self.game)
                if len(action) == 2:
                    return spawnaction_convertor(action)
                else:
                    return spreadaction_convertor(action)



    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                
                action = spawn_convertor(cell)
                self.game = take_action(action, self.game)
                pass

            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")

                action = spread_convertor(direction, cell)
                self.game = take_action(action, self.game)
                pass

