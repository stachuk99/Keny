import pygame

WIDTH, HEIGHT = 720, 720
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 40, 255)
RED = (255, 40, 40)
DARK_GREY = (128, 128, 128)
LIGHT_GREY = (210, 210, 210)
GOLD = (255, 215, 0)
LIGHT_GREEN = (144, 238, 144)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (int(SQUARE_SIZE * 0.4), int(SQUARE_SIZE * 0.3)))
