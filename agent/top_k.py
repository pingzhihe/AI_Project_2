from .game_class import Game, take_action
import heapq
def aminimax(game: Game, player: str, depth: int, alpha: float, beta: float):
    if depth == 0:
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


def find_best_move(game: Game, k: int = 3) -> tuple:
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    legal_actions = game.get_legal_action()
    top_k_scores = []

    for action in legal_actions:
        next_state = take_action(action, game)
        score = aminimax(next_state, "MIN", depth=3, alpha=alpha, beta=beta)

        if len(top_k_scores) < k:
            heapq.heappush(top_k_scores, (score, action))
        else:
            heapq.heappushpop(top_k_scores, (score, action))

    while top_k_scores:
        score, action = heapq.heappop(top_k_scores)
        if score > best_score:
            best_score = score
            best_move = action
        alpha = max(alpha, best_score)

    return best_move

def evaluate(game: Game, player: str):
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    if player == 'r':
        return (power_r - power_b)
    else:
        return (power_b - power_r) 