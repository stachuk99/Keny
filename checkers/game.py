from .constants import *
from .board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win, self.valid_moves)
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = []
        self.mandatory_moves = []
        self.turns_without_capture = 0

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.mandatory_moves = self.board.get_mandatory_moves(piece.color)
                self.valid_moves = self.board.get_valid_moves(piece)
                if self.mandatory_moves:
                    self.valid_moves = [x for x in self.valid_moves if x in self.mandatory_moves]
                return True

        return False


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        move = False
        for x in self.valid_moves:
            if x.destination == (row, col):
                move = x
        if self.selected and piece == 0 and move:
            self.board.move(self.selected, row, col)
            if move.captured and move.captured[0].color != self.selected.color:
                self.turns_without_capture = 0
                self.board.remove(move.captured)
            else:
                self.turns_without_capture += 1
                if self.turns_without_capture >= 10:
                    self.board.tie = "DRAW"

            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = []
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
