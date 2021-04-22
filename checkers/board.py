from copy import copy

from .constants import *
from .piece import Piece
from .move import move


class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 16
        self.turns_without_capture = 0
        self.tie = None
        self.create_board()

    def remove(self, pieces):
        for r, c in pieces:
            piece = self.get_piece(r, c)
            self.board[r][c] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                if piece.color == WHITE:
                    self.white_left -= 1

    def winner(self):
        if self.tie:
            return self.tie
        elif self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE
        else:
            return None

    def move(self, move):
        start_r, start_c = move.start
        dest_r, dest_c = move.destination
        piece = self.get_piece(start_r, start_c)
        self.board[start_r][start_c] = 0
        self.board[dest_r][dest_c] = piece
        if move.captured:
            if self.get_piece(*move.captured[0]).color != piece.color:
                self.turns_without_capture = 0
                self.remove(move.captured)
            else:
                self.turns_without_capture += 1
                if self.turns_without_capture >= 10:
                    self.tie = "DRAW"
        else:
            self.turns_without_capture += 1
            if self.turns_without_capture >= 10:
                self.tie = "DRAW"

        piece.move(dest_r, dest_c)
        if dest_r == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
        if dest_r == 0 and piece.color == BLACK:
            piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self, color):
        x = [item for subl in self.board for item in subl if item != 0 and item.color == color]
        return x

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, LIGHT_GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_valid_moves(self, win, moves):
        for move in moves:
            row, col = move.destination
            pygame.draw.circle(win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                               SQUARE_SIZE * 0.2)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if 0 < row < 3:
                    self.board[row].append(Piece(row, col, WHITE))
                elif 4 < row < 7:
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0)

    def draw(self, win, valid_moves):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        self.draw_valid_moves(win, valid_moves)

    def is_valid_position(self, row, col):
        if 0 <= row < ROWS and COLS > col >= 0:
            return True
        return False

    def get_mandatory_moves(self, color):
        moves = self.get_all_moves(color)
        mandatory_moves = []
        for move in moves:
            if move.captured and self.get_piece(*move.captured[0]).color != color:
                mandatory_moves.append(move)
        return mandatory_moves

    def get_all_moves(self, color):
        all_pieces = self.get_all_pieces(color)
        all_moves = []
        for p in all_pieces:
            moves = self.get_valid_moves(p)
            all_moves += moves
        return all_moves

    def get_valid_moves(self, piece):
        col = piece.col
        row = piece.row
        moves = self._move(row, col, piece)
        return moves

    def _move(self, row, col, piece, capture=False, leap=False, last=None):
        if last is None:
            last = []
        directions = {WHITE: [(row, col + 1), (row, col - 1), (row + 1, col)],
                      BLACK: [(row, col + 1), (row, col - 1), (row - 1, col)],
                      'king': [(row, col + 1), (row, col - 1), (row - 1, col), (row + 1, col)]}
        moves = []
        if piece.king:
            directions = directions['king']
        else:
            directions = directions[piece.color]

        for r, c in directions:
            if self.is_valid_position(r, c):
                p = self.get_piece(r, c)
                next_r, next_c = (r - (row - r), c - (col - c))
                if p == 0:
                    if not leap and not capture:
                        moves.append(move((piece.row, piece.col), (r, c), None))
                elif self.is_valid_position(next_r, next_c) and self.get_piece(next_r, next_c) == 0 and (
                        r, c) not in last:
                    l = copy(last)
                    l.append((r, c))
                    if capture and p.color != piece.color and not leap:
                        moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                        moves += self._move(next_r, next_c, piece, True, False, l)
                    elif leap and p.color == piece.color:
                        moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                        moves += self._move(next_r, next_c, piece, False, True, l)
                    elif not capture and not leap:
                        moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                        moves += self._move(next_r, next_c, piece, p.color != piece.color, p.color == piece.color, l)
        if piece.color == WHITE:
            r, c = (row - 1, col)
        else:
            r, c = (row + 1, col)
        if not piece.king and self.is_valid_position(r, c):
            p = self.get_piece(r, c)
            next_r, next_c = (r - (row - r), c - (col - c))
            if self.is_valid_position(next_r, next_c) and self.get_piece(next_r, next_c) == 0 \
                    and p != 0 and (r, c) not in last and p.color != piece.color and not leap:
                l = copy(last)
                l.append((r, c))
                moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                moves += self._move(next_r, next_c, piece, capture=True, leap=False, last=l)
        return moves
