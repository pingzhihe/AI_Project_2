from enum import Enum

class NodeType(Enum):
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, game_hash, score, depth, best_move, node_type):
        self.table[game_hash] = (score, depth, best_move, node_type)

    def retrieve(self, game_hash, depth):
        if game_hash in self.table and self.table[game_hash][1] >= depth:
            return self.table[game_hash]
        return None

    def clear(self):
        self.table.clear()