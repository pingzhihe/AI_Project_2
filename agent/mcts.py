
from referee.game import Board, SpawnAction, HexPos, SpreadAction, HexDir,Action
from .boardupdate import spawn_board, spread_board,render_board, apply_ansi,\
    get_legal_spawn, get_legal_spread
from .game_class import Game
import random
import math



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



def reset_game(game: Game):
    game.state = {}
    game.action_count = 0
    game.turn = 'r'
    


class Node:
    def __init__(self, game: Game, parent = None):
        self.game = game
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0
    
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
        child = Node(child_game, self)
        self.children.append(child)
        return child
    
    def update(self, result):
        self.visits += 1
        self.score += result


def monte_carlo_tree_search(game: Game, interations:int, exploration_constant = 1)->Node:
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


