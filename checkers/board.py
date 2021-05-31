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
        self.turn = 0
        self.last_move = None
        self.create_board()

    def remove(self, pieces):
        for r, c in pieces:
            piece = self.get_piece(r, c)
            self.board[r][c] = 0
            if piece != 0:
                if piece.is_white:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

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
        self.turn += 1
        self.last_move = move
        start_r, start_c = move.start
        dest_r, dest_c = move.destination
        piece = self.get_piece(start_r, start_c)
        self.board[start_r][start_c] = 0
        self.board[dest_r][dest_c] = piece
        if move.captured:
            if self.get_piece(*move.captured[0]).is_white != piece.is_white:
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
        if dest_r == ROWS - 1 and piece.is_white:
            piece.make_king()
        if dest_r == 0 and not piece.is_white:
            piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self, is_white):
        x = [item for subl in self.board for item in subl if item != 0 and item.is_white == is_white]
        return x

    def _draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, LIGHT_GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def _draw_valid_moves(self, win, moves):
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
                    self.board[row].append(Piece(row, col, WHITE, True))
                elif 4 < row < 7:
                    self.board[row].append(Piece(row, col, BLACK, False))
                else:
                    self.board[row].append(0)

    def draw(self, win, valid_moves):
        self._draw_squares(win)
        self._draw_last_move(win)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        self._draw_valid_moves(win, valid_moves)

    def _draw_last_move(self, win):
        if self.last_move:
            pygame.draw.rect(win, LIGHT_GREEN, (self.last_move.destination[1] * SQUARE_SIZE, self.last_move.destination[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, LIGHT_GREEN, (self.last_move.start[1] * SQUARE_SIZE, self.last_move.start[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def is_valid_position(self, row, col):
        if 0 <= row < ROWS and COLS > col >= 0:
            return True
        return False

    def get_mandatory_moves(self, is_white):
        moves = self._get_all_moves(is_white)
        mandatory_moves = []
        for move in moves:
            if move.captured and self.get_piece(*move.captured[0]).is_white != is_white:
                mandatory_moves.append(move)
        if not mandatory_moves:
            mandatory_moves = moves
        return mandatory_moves

    def _get_all_moves(self, is_white):
        all_pieces = self.get_all_pieces(is_white)
        all_moves = []
        for p in all_pieces:
            moves = self.get_valid_moves(p)
            all_moves += moves
        return all_moves

    def get_valid_moves(self, piece):
        col = piece.col
        row = piece.row
        moves = self._move(row, col, piece, capture=False, leap=False, last=[])
        return moves

    def _move(self, row, col, piece, capture=False, leap=False, last=None):
        moves = []
        if piece.king:
            directions = [(row, col + 1), (row, col - 1), (row - 1, col), (row + 1, col)]
        elif piece.is_white:
            directions = [(row, col + 1), (row, col - 1), (row + 1, col)]
        else:
            directions = [(row, col + 1), (row, col - 1), (row - 1, col)]

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
                    same_color = p.is_white == piece.is_white
                    if capture and not same_color and not leap:
                        moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                        moves += self._move(next_r, next_c, piece, True, False, l)
                    elif leap and same_color:
                        moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                        moves += self._move(next_r, next_c, piece, False, True, l)
                    elif not capture and not leap:
                        moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                        moves += self._move(next_r, next_c, piece, not same_color, same_color, l)
        if piece.is_white:
            r, c = (row - 1, col)
        else:
            r, c = (row + 1, col)
        if not piece.king and self.is_valid_position(r, c):
            p = self.get_piece(r, c)
            next_r, next_c = (r - (row - r), c - (col - c))
            if self.is_valid_position(next_r, next_c) and self.get_piece(next_r, next_c) == 0 \
                    and p != 0 and (r, c) not in last and p.is_white != piece.is_white and not leap:
                l = copy(last)
                l.append((r, c))
                moves.append(move((piece.row, piece.col), (next_r, next_c), l))
                moves += self._move(next_r, next_c, piece, capture=True, leap=False, last=l)
        return moves

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.board == other.board and self.turn == other.turn and self.last_move == other.last_move:
                return True

        else:
            return False
