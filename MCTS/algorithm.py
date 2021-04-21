import checkers.board
from copy import deepcopy
class MCTS:

    def __init__(self, color):
        self.color = color
        pass

    def move(self, board):
        board = deepcopy(board)
        moves = board.get_mandatory_moves(self.color)
        if not moves:
            moves = board.get_all_moves(self.color)
        for move in moves:
            pass

    def random_move(self, board, color):
        if board.winner():
            if board.winner == self.color:
                return 1
            elif board.winner == "DRAW":
                return 0.5
            else:
                return 0
        board = deepcopy(board)
        moves = board.get_mandatory_moves(self.color)
        if not moves:
            moves = board.get_all_moves(self.color)
        '''
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                skipped = filter(lambda x: x != 0 and x.color != self.selected.color, skipped)
                self.turns_without_capture = 0
                self.board.remove(skipped)
            else:
                self.turns_without_capture += 1
                if self.turns_without_capture >= 10:
                    self.board.tie = "DRAW"

            self.change_turn()
        else:
            return False

        return True'''
