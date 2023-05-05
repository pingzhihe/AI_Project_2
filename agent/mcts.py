
from referee.game import Board, SpawnAction, HexPos, SpreadAction, HexDir,Action
from .boardupdate import spawn_board, spread_board,render_board, apply_ansi,\
    get_legal_spawn, get_legal_spread
from .game_class import Game, take_action
import random
import math


def reset_game(game: Game):
    game.state = {}
    game.action_count = 0
    game.turn = 'r'
    
class Node:
    def __init__(self, game: Game, parent = None, transposition_table = None):
        self.game = game
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0
        self.transposition_table = transposition_table or {}
        self.transposition_table[game.get_hash()] = self    
    
    def is_fully_expanded(self) -> bool:
        return len(self.children) == len(self.game.get_legal_action())
    
    def get_best_child(self, exploration_constant):
        best_score = -math.inf
        best_child = None
        #The score is for the UCT (Upper Confidence Bound for Trees) 
        for child in self.children:
            score = child.score / child.visits + exploration_constant * math.sqrt(math.log(self.visits)/child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def add_child(self, child_game: Game):
        if child_game.get_hash() in self.transposition_table:
            child = self.transposition_table[child_game.get_hash()]
            child.parent = self
        else:
            child = Node(child_game, self, self.transposition_table)
        self.children.append(child)
        return child
    
    def update(self, result):
        self.visits += 1
        self.score += result


def monte_carlo_tree_search(game: Game, interations:int, exploration_constant = 3)->Node:
    root = Node(game)

    for _ in range(interations):
        #The selection part
        node = root
        if len(node.children) != 0:
            while not (node.is_fully_expanded()) and not (node.game.is_terminal()):
                if len(node.children) == 0:
                    break
                node = node.get_best_child(exploration_constant)

        #The expansion part
        if not node.game.is_terminal():
            #Get the node which is unexplored
            action = random.choice(list(set(node.game.get_legal_action()) - set(child.game.action for child in node.children)))
            node = node.add_child(take_action(action, node.game))

        #The simulation part
        current_game = node.game
        while(not current_game.is_terminal()):
            action = random.choice(current_game.get_legal_action())
            current_game =take_action(action, take_action(action, current_game))

        #The backpropagation part
        result = current_game.get_result(root.game.player)
        while node:
            node.update(result)
            node = node.parent
    
    return root.get_best_child(exploration_constant)


