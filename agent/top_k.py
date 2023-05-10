from .game_class import Game, take_action

def aminimax(game: Game, player: str, depth: int, alpha: float, beta: float, k: int):
    if depth == 0 or game.is_terminal():
        return evaluate(game, game.player)

    legal_actions = game.get_legal_action()
    sorted_actions = sorted(legal_actions, key=lambda action: evaluate(take_action(action, game), player), reverse=(player == "MAX"))
    top_k_actions = sorted_actions[:k]

    if player == "MAX":
        best_score = float('-inf')
        for action in top_k_actions:
            next_state = take_action(action, game)
            score = aminimax(next_state, "MIN", depth - 1, alpha, beta, k)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for action in top_k_actions:
            next_state = take_action(action, game)
            score = aminimax(next_state, "MAX", depth - 1, alpha, beta, k)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def ab_find_best_move_top_k(game: Game, k: int) -> tuple:
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for action in game.get_legal_action():
        next_state = take_action(action, game)
        score = aminimax(next_state, "MIN", depth = 3, alpha=alpha, beta=beta, k=k)
        if score > best_score:
            best_score = score
            best_move = action
        alpha = max(alpha, best_score)
    return best_move

def evaluate(game: Game, player: str) -> float:
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    if player == 'r':
        return power_r - power_b
    else:
        return power_b - power_r