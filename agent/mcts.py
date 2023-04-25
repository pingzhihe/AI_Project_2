import math
import random

class Node:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_legal_actions())

    def get_best_child(self, exploration_constant):
        best_score = -math.inf
        best_child = None
        for child in self.children:
            score = child.score / child.visits + exploration_constant * math.sqrt(math.log(self.visits) / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.score += result



def monte_carlo_tree_search(game_state, iterations, exploration_constant=1):
    root = Node(game_state)

    for _ in range(iterations):
        # Selection
        node = root
        while not node.is_fully_expanded() and not node.game_state.is_terminal():
            node = node.get_best_child(exploration_constant)

        # Expansion
        if not node.game_state.is_terminal():
            action = random.choice(list(set(node.game_state.get_legal_actions()) - set(child.game_state for child in node.children)))
            node = node.add_child(node.game_state.perform_action(action))

        # Simulation
        current_game = node.game_state
        while not current_game.is_terminal():
            action = random.choice(current_game.get_legal_actions())
            current_game = current_game.perform_action(action)

        # Backpropagation
        result = current_game.get_result(node.game_state.current_player)
        while node:
            node.update(result)
            node = node.parent

    return root.get_best_child(exploration_constant)