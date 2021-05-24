from copy import deepcopy
from checkers.constants import WHITE, BLACK

import anytree
import itertools
import random
import math

RANDOM_TESTS = 80
INITIAL_SIMULATION = 2



class MCTS:

    def __init__(self, is_white):
        self.color = is_white
        self.tree = None
        self.index = itertools.count(1)

    # base on MTCS algoritm make best move
    def move(self, board):
        moves = board.get_mandatory_moves(self.color)

        if self.tree is None:
            self.tree = anytree.Node("root", children=[], board=None, move=None, wins=0, simulations=1, color=not self.color)
        else:
            self.tree = anytree.search.find_by_attr(self.tree,  name="board", value=board, maxlevel=3)
            self.tree.parent = None
            self.tree.move = None
            self.tree.wins = 0
            self.tree.simulations = 1

        #self.tree = anytree.Node("root", children=[], board=None, move=None, wins=0, simulations=1,
                                 #color=not self.color)
        for pre, _, node in anytree.RenderTree(self.tree, maxlevel=2):
            print(
                "%s %s->(%s/%s --> %s%%)" % (pre, node.move, node.wins, node.simulations, node.wins / node.simulations))

        for move in moves:
            b = deepcopy(board)
            b.move(move)
            if not anytree.search.find_by_attr(self.tree, value=board, name="board", maxlevel=2):
                node = anytree.Node(str(next(self.index)), parent=self.tree,
                                    children=[], board=b, move=move, wins=0, simulations=0, color=self.color)

                result = 0
                for i in range(INITIAL_SIMULATION):
                    result += self._simulation(deepcopy(b), self.color)
                self._back_propagation(node, result, INITIAL_SIMULATION)

        for _ in range(RANDOM_TESTS):
            node = self._selection()
            self._expansion(node)
            for n in node.children:
                result = 0
                for i in range(INITIAL_SIMULATION):
                    result += self._simulation(deepcopy(n.board), n.color)
                self._back_propagation(n, result, INITIAL_SIMULATION)
            print(_)
            for pre, _, node in anytree.RenderTree(self.tree, maxlevel=2):
                print("%s %s->(%s/%s --> %s%%)" % (pre, node.move, node.wins, node.simulations, node.wins / node.simulations))

        best_node = None
        max_simulations = 0
        for n in self.tree.children:
            if n.simulations > max_simulations:
                best_node = n
                max_simulations = n.simulations

        return best_node.move

    # choose best node based on UCT
    def _selection(self):
        node = self.tree
        best_node = node
        while node.children:
            best_result = -1
            nv = 0
            for c in node.children:
                nv += c.simulations
            for c in node.children:
                if c.wins / c.simulations + 1.41 * math.sqrt(math.log(nv) / c.simulations) > best_result:
                    best_node = c
                    best_result = c.wins / c.simulations + 1.41 * math.sqrt(math.log(nv) / c.simulations)
            node = best_node
        return best_node

    def _expansion(self, node):
        if node.board.winner():
            return None
        else:
            moves = node.board.get_mandatory_moves(not node.color)
            for move in moves:
                b = deepcopy(node.board)
                b.move(move)
                anytree.Node(str(next(self.index)), parent=node,
                                    children=[], board=b, move=move, wins=0, simulations=0, color=not node.color)


    # updates nodes base on results
    def _back_propagation(self, node, result, simulations):
        while node.parent:
            node.simulations += simulations
            if node.color == self.color:
                node.wins += result
            else:
                node.wins += simulations - result
            node = node.parent

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
        moves = board.get_mandatory_moves(color)
        if not moves:
            return 0.5
        move = random.choice(moves)
        board.move(move)
        color = not color
        return self._simulation(board, color)
