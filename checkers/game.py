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
        self.valid_moves = {}
        self.mandatory_moves = {}
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
                all_pieces = self.board.get_all_pieces(piece.color)
                self.mandatory_moves = {}
                for p in all_pieces:
                    moves = self.board.get_valid_moves(p)
                    for item in moves.items():
                        if item[1][0] != 0 and item[1][0].color != piece.color :
                            #self.mandatory_moves[p].append(((item[0][0], item[0][1]), item[1]))
                            self.mandatory_moves.setdefault(p, []).append((item[0][0], item[0][1]))
                self.valid_moves = self.board.get_valid_moves(piece)
                if self.mandatory_moves:
                    print(self.mandatory_moves.get(piece))
                    if self.mandatory_moves.get(piece):
                        x = self.mandatory_moves.get(piece)
                        self.valid_moves = {item[0] : item[1] for item in self.valid_moves.items() if item[0] in self.mandatory_moves.get(piece)}
                    else:
                        self.valid_moves = []
                        self.selected = None
                return True

        return False

    def _move(self, row, col):
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

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
