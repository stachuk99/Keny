from copy import deepcopy
from checkers.constants import WHITE, BLACK

import anytree
import itertools
import math
import random
import time

N0 = 15

class MCTS:
    def __init__(self, white, simulation_time):
        self.color = white
        self.tree = None
        self.simulation_time = simulation_time
        self.index = itertools.count(1)

    # return best move base on MTCS algorithm
    def move(self, board, return_move):
        moves = board.get_moves(self.color)

        if self.tree is None:
            self.tree = anytree.Node("root", children=[], board=deepcopy(board), move=None, wins=0, simulations=0,
                                     moves_left=moves, color=not self.color)
        else:
            self.tree = anytree.search.find_by_attr(self.tree,  name="board", value=board, maxlevel=3)
            if self.tree is None:
                self.tree = anytree.Node("root", children=[], board=deepcopy(board), move=None, wins=0, simulations=0,
                                         moves_left=moves, color=not self.color)
            else:
                self.tree.parent = None

        start = time.time()
        i = 0
        while time.time() - start < self.simulation_time:
            selected_node = self._selection()
            expansion_node = self._expansion(selected_node)
            result = self._simulation(deepcopy(expansion_node.board), expansion_node.color)
            self._back_propagation(expansion_node, result, 1)
            i += 1
            if i % 100 == 0:
                print(i)
                for pre, _, node in anytree.RenderTree(self.tree, maxlevel=2):
                    print("%s %s->(%s/%s --> %s%%)" % (pre, node.move, node.wins, node.simulations, node.wins / node.simulations))

        best_node = None
        max_simulations = 0
        for n in self.tree.children:
            if n.simulations > max_simulations:
                best_node = n
                max_simulations = n.simulations
        return_move.append(best_node.move)
        return

    # choose best node based on UCT
    def _selection(self):
        node = self.tree
        best_node = node
        i = 0
        while not node.moves_left:
            if node.board.winner():
                return node
            best_result = -1
            nv = 0
            for c in node.children:
                nv += c.simulations
            for c in node.children:
                if c.wins / c.simulations + 1.41 * math.sqrt(math.log(nv) / c.simulations) > best_result:
                    best_node = c
                    best_result = c.wins / c.simulations + 1.41 * math.sqrt(math.log(nv) / c.simulations)
            node = best_node
            i += 1
        return best_node

    # expands tree if algorithm conditions are met
    def _expansion(self, node):
        if node.board.winner():
            return node
        else:
            if node.simulations > N0:
                move = node.moves_left.pop()
                b = deepcopy(node.board)
                b.move(move)
                moves_left = b.get_moves(node.color)
                node = anytree.Node(str(next(self.index)), parent=node, children=[],
                             board=b, move=move, wins=0, simulations=0,moves_left=moves_left, color=not node.color)
            return node

    # updates nodes based on results
    def _back_propagation(self, node, result, simulations):
        while not node.is_root:
            node.simulations += simulations
            if node.color == self.color:
                node.wins += result
            else:
                node.wins += simulations - result
            node = node.parent
        self.tree.simulations += simulations
        self.tree.wins += simulations - result

    # plays a random game
    def _simulation(self, board, color):
        if board.winner():
            if board.winner() == WHITE:
                if self.color:
                    return 1
                return 0
            elif board.winner() == BLACK:
                if self.color:
                    return 0
                return 1
            else:
                return 0.5
        moves = board.get_moves(color)
        if not moves:
            return 0.5
        move = random.choice(moves)
        board.move(move)
        color = not color
        return self._simulation(board, color)
