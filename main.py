import pgu
import pygame
import checkers.constants as c
from checkers.board import Board
from checkers.game import Game
from MCTS import algorithm
from copy import deepcopy
from pgu import gui

FPS = 60
pygame.init()

TNR32=pygame.font.SysFont('timesnewroman', 32)
TNR36=pygame.font.SysFont('timesnewroman', 36)

white_player = True
black_player = True
white_player_time = 30
black_player_time = 30

start_screen = gui.Desktop()
start_screen.connect(gui.QUIT,start_screen.quit,None)

table = gui.Table(x=0, y=0, font=TNR32)
table.tr()
table.td(gui.Label("Czarny", font=TNR32), colspan=1)
table.td(gui.Label("Biały", font=TNR32), colspan=3)

table.tr()


black_player_select = gui.Select(False, width=150, height=70, font=TNR32)
black_player_select.add(gui.Label('Komputer',font=TNR32), True)
black_player_select.add(gui.Label('Gracz',font=TNR32), False)
table.td(black_player_select, colspan=1)
table.td(gui.Label())
white_player_select = gui.Select(False, width=150, height=70, font=TNR32)
white_player_select.add(gui.Label('Komputer',font=TNR32), True)
white_player_select.add(gui.Label('Gracz',font=TNR32), False)
table.td(white_player_select, colspan=3)


table.tr()
table.td(gui.Label())
table.tr()


table.td(gui.Label("     Czas wyznaczania ruchu", font=TNR32), colspan=3)
table.tr()

black_time_select = gui.Select(30, width=130, height=70)
black_time_select.add(gui.Label('30s',font=TNR32), 30)
black_time_select.add(gui.Label('60s',font=TNR32), 60)
black_time_select.add(gui.Label('90s',font=TNR32), 90)
black_time_select.resize(130,70)

table.td(black_time_select, colspan=1, x=400, y=200)

table.td(gui.Label())
white_time_select = gui.Select(30, width=130, height=70)
white_time_select.add(gui.Label('30s',font=TNR32), 30)
white_time_select.add(gui.Label('60s',font=TNR32), 60)
white_time_select.add(gui.Label('90s',font=TNR32), 90)
table.td(white_time_select, colspan=3)

table.tr()
table.td(gui.Label())
table.tr()
table.td(gui.Label())
table.tr()

def start_game():
    global white_player
    white_player = white_player_select.value
    global black_player
    black_player = black_player_select.value
    global white_player_time
    white_player_time = white_time_select.value
    global black_player_time
    black_player_time = black_time_select.value
    start_screen.quit()

w = gui.Button(value=gui.Label('Rozpocznij gre',font=TNR36), width=200, height=100)
w.connect(gui.CLICK, start_game)
table.td(w, colspan=6)

start_screen.init(table)
start_screen.run()

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption('Keny')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // c.SQUARE_SIZE
    col = x // c.SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    white_mcts = None
    black_mcts = None
    if white_player:
        white_mcts = algorithm.MCTS(True, white_player_time)
    if black_player:
        black_mcts = algorithm.MCTS(False, black_player_time)
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
            if white_mcts:
                game.ai_move(white_mcts.move(deepcopy(game.board)))
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        game.select(row, col)
        else:
            if black_mcts:
                game.ai_move(black_mcts.move(deepcopy(game.board)))
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

