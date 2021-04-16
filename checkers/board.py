from copy import copy

import pygame
from .constants import *
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 16
        self.black_kings = self.white_kings = 0
        self.create_board()

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                if piece.color == WHITE:
                    self.white_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return WHITE
        elif self.black_left <= 0:
            return BLACK
        else:
            return None

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
            self.white_kings += 1
        if row == 0 and piece.color == BLACK:
            piece.make_king()
            self.black_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, LIGHT_GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_valid_moves(self, win, moves):
        for move in moves:
            row, col = move
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

    def get_valid_moves(self, piece):
        moves = {}
        col = piece.col
        row = piece.row
        moves.update(self._move(row, col, piece))
        return moves

    def _move(self, row, col, piece, capture=False, leap=False, last=None):
        if last == None:
            last = []
        directions = {WHITE: [(row, col + 1), (row, col - 1), (row + 1, col)],
                      BLACK: [(row, col + 1), (row, col - 1), (row - 1, col)],
                      'king': [(row, col + 1), (row, col - 1), (row - 1, col), (row + 1, col)]}
        moves = {}
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
                        moves[(r, c)] = p
                elif self.is_valid_position(next_r, next_c) and self.get_piece(next_r,next_c) == 0 and p not in last:
                    if capture and p.color != piece.color:
                        last.append(p)
                        moves[(next_r, next_c)] = copy(last)
                        moves.update(self._move(next_r, next_c, piece, True, False, last))
                    elif leap and p.color == piece.color:
                        last.append(p)
                        moves[(next_r, next_c)] = copy(last)
                        moves.update(self._move(next_r, next_c, piece, False, True, last))
                    elif not capture and not leap:
                        last.append(p)
                        moves[(next_r, next_c)] = copy(last)
                        moves.update(self._move(next_r, next_c, piece, p.color != piece.color, p.color == piece.color, last))
        if piece.color == WHITE:
            r, c = (row - 1, col)
        else:
            r, c = (row + 1, col)
        if not piece.king and self.is_valid_position(r, c):
            p = self.get_piece(r, c)
            next_r, next_c = (r - (row - r), c - (col - c))
            if self.is_valid_position(next_r, next_c) and self.get_piece(next_r,next_c) == 0\
                    and p != 0 and p not in last and p.color != piece.color:
                last.append(p)
                moves[(next_r, next_c)] = copy(last)
                moves.update(self._move(next_r, next_c, piece, True, False, last))
        return moves
