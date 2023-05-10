from .game_class import Game, take_action

def aminimax(game: Game, player: str, depth: int, alpha: float, beta: float):
    if depth == 0 or game.is_terminal():
        return evaluate(game, game.player), None

    best_move = None
    if player == "MAX":
        best_score = float('-inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score, _ = aminimax(next_state, "MIN", depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = action
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
    else:
        best_score = float('inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score, _ = aminimax(next_state, "MAX", depth - 1, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = action
            beta = min(beta, best_score)
            if beta <= alpha:
                break

    return best_score, best_move

def iterative_deepening_search(game: Game, max_depth: int):
    best_move = None
    for depth in range(1, max_depth + 1):
        _, move = aminimax(game, "MAX", depth, float('-inf'), float('inf'))
        if move is not None:
            best_move = move
    return best_move

def ab_find_best_move_ids(game: Game, max_depth: int) -> tuple:
    return iterative_deepening_search(game, max_depth)

def evaluate(game: Game, player: str) -> float:
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    if player == 'r':
        return power_r - power_b
    else:
        return power_b - power_r
