import pygame
import checkers.constants as c
from checkers.board import Board
from checkers.game import Game
from MCTS import algorithm
from copy import deepcopy
import time

FPS = 60

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption('Keny')
pygame.init()


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // c.SQUARE_SIZE
    col = x // c.SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    mtcs = algorithm.MCTS(True)
    game.update()
    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            game.display_result(WIN)
            pygame.display.update()
            wait_for_reset = True
            while wait_for_reset:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        game.reset()
                        game.update()
                        pygame.display.update()
                        wait_for_reset = False
                    if event.type == pygame.QUIT:
                        wait_for_reset = False
                        run = False

        if game.turn == c.WHITE:
            game.ai_move(mtcs.move(deepcopy(game.board)))

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()

    pygame.quit()


main()
