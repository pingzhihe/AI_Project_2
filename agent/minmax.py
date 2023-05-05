from .game_class import Game, take_action
import random
    
def aminimax(game: Game, player: str, depth: int):
    if depth == 0:
        return evaluate(game, game.player)
    if player == "MAX":
        best_score = float('-inf')
        action_list = game.get_legal_action()
        random.shuffle(action_list)
        for action in action_list:
            next_state = take_action(action, game)
            score = aminimax(next_state, "MIN", depth - 1)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        action_list = game.get_legal_action()
        random.shuffle(action_list)
        for action in action_list:
            next_state = take_action(action, game)
            score = aminimax(next_state, "MAX", depth - 1)
            best_score = min(best_score, score)
        return best_score
    

def mx_find_best_move(game: Game) -> tuple:
    best_score = float('-inf')
    best_move = None
    for action in game.get_legal_action():
        next_state = take_action(action, game)
        score = aminimax(next_state, "MIN", depth=2)
        if score > best_score:
            best_score = score
            best_move = action
    return best_move




def evaluate(game: Game, player: str):
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    if player == 'r':
        return power_r - power_b
    else:
        return power_b - power_r

