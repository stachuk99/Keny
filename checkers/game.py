import time

from .constants import *
from .board import Board
import pygame

pygame.init()
font72 = pygame.font.SysFont('timesnewroman', 72)
font48 = pygame.font.SysFont('timesnewroman', 48)
TNR32=pygame.font.SysFont('timesnewroman', 32)

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.turn_time = time.time()

    def update(self):
        self.board.draw(self.win, self.valid_moves)
        time_text = TNR32.render(str(int(time.time() - self.turn_time)), True, GOLD)
        time_text_rec = time_text.get_rect()
        time_text_rec.center = (WIDTH - 25, 25)
        self.win.blit(time_text, time_text_rec)
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = []

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
                mandatory_moves = self.board.get_moves(piece.is_white)
                self.valid_moves = self.board._get_valid_moves(piece)
                if mandatory_moves:
                    self.valid_moves = [x for x in self.valid_moves if x in mandatory_moves]
                return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        move = False
        for x in self.valid_moves:
            if x.destination == (row, col):
                move = x
        if self.selected and piece == 0 and move:
            self.board.move(move)
            self.turn_time = time.time()
            self._change_turn()
        else:
            return False
        return True

    def ai_move(self, move):
        self.board.move(move)
        self.turn_time = time.time()
        self._change_turn()

    def _change_turn(self):
        self.valid_moves = []
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def display_result(self, WIN):
        if self.winner() == "DRAW":
            text1 = font72.render('REMIS', True, GOLD)
            text2 = False
        elif self.winner() == WHITE:
            text1 = font72.render('WYGRA??', True, GOLD)
            text2 = font72.render('BIA??Y', True, GOLD)
        else:
            text1 = font72.render('WYGRA??', True, GOLD)
            text2 = font72.render('CZARNY', True, GOLD)
        text_rec1 = text1.get_rect()
        text_rec1.center = (WIDTH // 2, HEIGHT // 3)
        if text2:
            text_rec1.center = (WIDTH // 2, HEIGHT // 3 - 50)
            text_rec2 = text2.get_rect()
            text_rec2.center = (WIDTH // 2, HEIGHT // 3 + 50)
            WIN.blit(text2, text_rec2)
        new_game_text1 = font48.render('WCI??NIJ DOWOLNY PRZYCISK', True, GOLD)
        new_game_text_rec1 = new_game_text1.get_rect()
        new_game_text_rec1.center = (WIDTH // 2, HEIGHT // 2 + 150)
        new_game_text2 = font48.render(' ABY ROZPOCZ???? NOW?? GR??', True, GOLD)
        new_game_text_rec2 = new_game_text2.get_rect()
        new_game_text_rec2.center = (WIDTH // 2, HEIGHT // 2 + 200)
        WIN.blit(text1, text_rec1)
        WIN.blit(new_game_text1, new_game_text_rec1)
        WIN.blit(new_game_text2, new_game_text_rec2)
