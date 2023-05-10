from .game_class import Game, take_action
from enum import Enum
from collections import OrderedDict

class NodeType(Enum):
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2



class TranspositionTable:
    def __init__(self, max_size=10000):
        self.max_size = max_size
        self.cache = OrderedDict()

    def store(self, game_hash, score, depth, best_move, node_type):
        if game_hash in self.cache:
            self.cache.pop(game_hash)
        self.cache[game_hash] = (score, depth, best_move, node_type)
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def retrieve(self, game_hash, depth):
        entry = self.cache.get(game_hash)
        if entry and entry[1] >= depth:
            # Update the LRU cache by moving the accessed entry to the end
            self.cache.move_to_end(game_hash)
            return entry
        return None

    def clear(self):
        self.cache.clear()


def aminimax(game: Game, player: str, depth: int, alpha: float, beta: float, transposition_table: TranspositionTable):
    game_hash = game.get_hash()
    stored_entry = transposition_table.retrieve(game_hash, depth)

    if stored_entry:
        stored_score, _, stored_move, stored_node_type = stored_entry
        if stored_node_type == NodeType.LOWER_BOUND:
            alpha = max(alpha, stored_score)
        elif stored_node_type == NodeType.UPPER_BOUND:
            beta = min(beta, stored_score)
        else:
            return stored_score, stored_move

        if alpha >= beta:
            return stored_score, stored_move

    if depth == 0 or game.is_terminal():
        score = evaluate(game, game.player)
        transposition_table.store(game_hash, score, depth, None, NodeType.EXACT)
        return score, None

    best_move = None
    node_type = NodeType.UPPER_BOUND
    if player == "MAX":
        best_score = float('-inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score, _ = aminimax(next_state, "MIN", depth - 1, alpha, beta, transposition_table)
            if score > best_score:
                best_score = score
                best_move = action
                node_type = NodeType.EXACT
            alpha = max(alpha, best_score)
            if beta <= alpha:
                node_type = NodeType.LOWER_BOUND
                break
    else:
        best_score = float('inf')
        for action in game.get_legal_action():
            next_state = take_action(action, game)
            score, _ = aminimax(next_state, "MAX", depth - 1, alpha, beta, transposition_table)
            if score < best_score:
                best_score = score
                best_move = action
                node_type = NodeType.EXACT
            beta = min(beta, best_score)
            if beta <= alpha:
                node_type = NodeType.UPPER_BOUND
                break

    transposition_table.store(game_hash, best_score, depth, best_move, node_type)
    return best_score, best_move

def iterative_deepening_search(game: Game, max_depth: int, transposition_table: TranspositionTable):
    best_move = None
    for depth in range(1, max_depth + 1):
        _, move = aminimax(game, "MAX", depth, float('-inf'), float('inf'), transposition_table)
        if move is not None:
            best_move = move
    return best_move

def ab_find_best_move_ids_tb(game: Game, max_depth: int, transposition_table: TranspositionTable) -> tuple:
    return iterative_deepening_search(game, max_depth, transposition_table)

def evaluate(game: Game, player: str) -> float:
    power_b = game.count_power('b')
    power_r = game.count_power('r')
    if player == 'r':
        return power_r - power_b
    else:
        return power_b - power_r

