from .game_class import Game, take_action

def aminimax(game: Game, player: str, depth: int, alpha: float, beta: float):
    if depth == 0 or game.is_terminal():
        return evaluate(game, game.player)
    
    if player == "MAX":
        best_score = float('-inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score = aminimax(next_state, "MIN", depth - 1, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score = aminimax(next_state, "MAX", depth - 1, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def ab_find_best_move(game: Game) -> tuple:
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for action in game.get_legal_action():
        next_state = take_action(action, game)
        score = aminimax(next_state, "MIN", depth = 2, alpha=alpha, beta=beta)
        if score > best_score:
            best_score = score
            best_move = action
        alpha = max(alpha, best_score)
    return best_move

def evaluate(game: Game, player: str):
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    token_b = game.count_token('b')
    token_r = game.count_token('r')
    if player == 'r':
        return power_r - power_b
    else:
        return power_b - power_r