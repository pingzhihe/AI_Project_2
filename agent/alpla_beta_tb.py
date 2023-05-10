from .game_class import Game, take_action
import math

def aminimax(game: Game, player: str, depth: int, alpha: float, beta: float, transposition_table: dict):
    game_hash = game.get_hash()

    if game_hash in transposition_table:
        stored_entry = transposition_table[game_hash]
        if stored_entry['depth'] >= depth:
            stored_type, stored_score = stored_entry['type'], stored_entry['score']
            if stored_type == 'EXACT':
                return stored_score
            if stored_type == 'LOWER' and stored_score > alpha:
                alpha = stored_score
            if stored_type == 'UPPER' and stored_score < beta:
                beta = stored_score
            if alpha >= beta:
                return stored_score

    if depth == 0 or game.is_terminal():
        score = evaluate(game, game.player)
    elif player == "MAX":
        score = float('-inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score = max(score, aminimax(next_state, "MIN", depth - 1, alpha, beta, transposition_table))
            alpha = max(alpha, score)
            if beta <= alpha:
                break
    else:  # player == "MIN"
        score = float('inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score = min(score, aminimax(next_state, "MAX", depth - 1, alpha, beta, transposition_table))
            beta = min(beta, score)
            if beta <= alpha:
                break

    if score <= alpha:
        transposition_table[game_hash] = {'depth': depth, 'score': score, 'type': 'UPPER'}
    elif score >= beta:
        transposition_table[game_hash] = {'depth': depth, 'score': score, 'type': 'LOWER'}
    else:
        transposition_table[game_hash] = {'depth': depth, 'score': score, 'type': 'EXACT'}

    return score


def ab_find_best_move_tb(game: Game, transposition_table: dict) -> tuple:
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    for action in game.get_legal_action():
        next_state = take_action(action, game)
        score = aminimax(next_state, "MIN", depth = 3, alpha=alpha, beta=beta, transposition_table=transposition_table)
        if score > best_score:
            best_score = score
            best_move = action
        alpha = max(alpha, best_score)
    return best_move

def evaluate(game: Game, player: str):
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    if player == 'r':
        return power_r - power_b
    else:
        return power_b - power_r