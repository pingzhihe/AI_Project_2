# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, Board



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
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
                self.action_list  = [HexPos(0,0),HexPos(1,1),HexPos(2,2)]
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
                self.action_list = [HexPos(4,4),HexPos(5,5),HexPos(6,6)]

        self.state = {}

        


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """ 

        match self._color:
            case PlayerColor.RED:
                self._index += 1
                self.state.apply_action(SpawnAction(self.action_list[self._index]))
                return SpawnAction(self.action_list[self._index])

            case PlayerColor.BLUE:
                self._index += 1
                # This is going to be invalid... BLUE never spawned!
                self.state.apply_action(SpawnAction(self.action_list[self._index]))
                return SpawnAction(self.action_list[self._index])

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass

