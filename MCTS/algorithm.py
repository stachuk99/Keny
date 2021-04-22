from copy import deepcopy
from checkers.constants import WHITE, BLACK

RANDOM_TESTS = 10

import random


class MCTS:

    def __init__(self, color):
        self.color = color
        pass

    def move(self, board):
        moves_rating = []
        moves = board.get_mandatory_moves(self.color)
        best_move = None
        best_rate = 0
        if not moves:
            moves = board.get_all_moves(self.color)
        for move in moves:
            rate = 0
            b = deepcopy(board)
            b.move(move)
            for i in range(RANDOM_TESTS):
                rate += self._random_move(deepcopy(b), self.color, 0)
            moves_rating.append((move, rate))
            if rate > best_rate:
                best_move = move
                best_rate = rate
        print(moves_rating)
        return best_move

    def _random_move(self, board, color, depht):
        if board.winner():
            x = board.winner()
            if board.winner() == self.color:
                return 1
            elif board.winner() == "DRAW":
                return 0.5
            else:
                return 0
        moves = board.get_mandatory_moves(color)
        if not moves:
            moves = board.get_all_moves(color)
        if not moves:
            print(" co xD")
        move = random.choice(moves)
        board.move(move)
        if color == WHITE:
            color = BLACK
        else:
            color = WHITE
        return self._random_move(board, color, depht + 1)
