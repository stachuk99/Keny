import pygame
from .constants import WHITE, DARK_GREY, SQUARE_SIZE, CROWN

PIECE_SIZE = 0.9
PADDING = 0.15


class Piece:
    def __init__(self, row, col, color, is_white):
        self.row = row
        self.col = col
        self.is_white = is_white
        self.color = color
        self.king = False
        self.radius = SQUARE_SIZE // 2 - SQUARE_SIZE * (1 - PIECE_SIZE)

    @staticmethod
    def calc_pos(row, col):
        x = SQUARE_SIZE * col + SQUARE_SIZE // 2
        y = SQUARE_SIZE * row + SQUARE_SIZE // 2
        return (x,y)

    def move(self, row, col):
        self.row = row
        self.col = col

    def make_king(self):
        self.king = True

    def draw(self, win):
        position = Piece.calc_pos(self.row, self.col)
        pygame.draw.circle(win, DARK_GREY, position, self.radius)
        pygame.draw.circle(win, self.color, position, self.radius * (1 - PADDING))
        if self.king:
            win.blit(CROWN, (position[0] - CROWN.get_width() // 2, position[1] - CROWN.get_height() // 2))

    def __repr__(self):
        if self.color == WHITE:
            return "W-" + str(self.row) + "-" + str(self.col)
        else:
            return "B-" + str(self.row) + "-" + str(self.col)
