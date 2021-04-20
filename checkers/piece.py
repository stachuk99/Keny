import pygame
from .constants import WHITE, DARK_GREY, SQUARE_SIZE, CROWN

PIECE_SIZE = 0.9
PADDING = 0.15


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.radius = SQUARE_SIZE // 2 - SQUARE_SIZE * (1 - PIECE_SIZE)

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def make_king(self):
        self.king = True

    def draw(self, win):
        pygame.draw.circle(win, DARK_GREY, (self.x, self.y,), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y,), self.radius * (1 - PADDING))
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def __repr__(self):
        if self.color == WHITE:
            return "W-" + str(self.row) + "-" + str(self.col)
        else:
            return "B-" + str(self.row) + "-" + str(self.col)
