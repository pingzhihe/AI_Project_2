from .boardupdate import get_legal_spawn, get_legal_spread, spawn_board, spread_board

class Game:
    def __init__(self):
        self.state = {}
        self.turn = 'r'
        self.action_count = 0
        self.player = None
        self.action = ()


    def count_power(self,color: str) -> int:
        power = 0
        for value in self.state.values():
            if value[0] == color:
                power += value[1]
        return power
    
    def get_legal_action(self)->list:
        action_list = []
        spread_list = []
        spawn_list = []
        spread_list = get_legal_spread(self.turn, self.state)
        spawn_list = get_legal_spawn(self.state)
        action_list = spread_list + spawn_list
        return action_list
    
    def is_terminal(self) ->bool:
        if self.action_count == 343:
            return True
        power_b = self.count_power('b')
        power_r = self.count_power('r')
        if self.action_count > 1:
            if power_b == power_b + power_r:
                return True
            elif power_r == power_b + power_r:
                return True
            else:
                return False

    def get_result(self, player: str) -> int:
        power_b = self.count_power('b')
        power_r = self.count_power('r')
        if player == 'r':
            if power_r == power_r + power_b:
                return 1
            elif power_b == power_r + power_b:
                return -1
            elif power_r -power_b >= 2:
                return 1
            elif power_b - power_r >=2:
                return -1
            else:
                return 0
        if player == 'b':
            if power_b == power_r + power_b:
                return 1
            elif power_r == power_r + power_b:
                return -1
            elif power_b - power_r >= 2:
                return 1
            elif power_r - power_b >= 2:
                return -1
            else:
                return 0
            
    def switch_turn(self) ->str:
        if self.turn == 'r':
            return 'b'
        else:
            return 'r'
        

def take_action(action: tuple, game: Game):
    new_game = Game()

    #A spawn action
    if len(action) == 2:
        new_game.state = spawn_board(game.state, action, game.turn)
    #A spread action
    else:
        new_game.state = spread_board(game.state, action, game.turn)
    new_game.action_count = game.action_count + 1
    new_game.action = action
    new_game.turn = game.switch_turn()
    return new_game
