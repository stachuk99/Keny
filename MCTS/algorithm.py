from copy import deepcopy
from checkers.constants import WHITE, BLACK

RANDOM_TESTS = 100

import random


class MCTS:

    def __init__(self, is_white):
        self.color = is_white
        pass

    def move(self, board):
        moves_rating = []
        moves = board.get_mandatory_moves(self.color)
        best_move = None
        best_rate = 0
        for move in moves:
            rate = 0
            b = deepcopy(board)
            b.move(move)
            for i in range(RANDOM_TESTS):
                rate += self._random_move(deepcopy(b), self.color)
            moves_rating.append((move, rate))
            if rate > best_rate:
                best_move = move
                best_rate = rate
        print(moves_rating)
        return best_move

    def _random_move(self, board, color):
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
        return self._random_move(board, color)
