import pygame
import numpy as np
import math

pygame.init()


def matrix_to_points(board, distance, reference):
    points = np.zeros((*board.shape, 2), int)
    (x_ref, y_ref) = reference
    for x, y in np.ndindex(board.shape):
        pxl_x = distance / 2 * (y - x) + x_ref
        pxl_y = math.cos(math.pi / 12) * distance * (y + x) + y_ref
        points[x, y, 0] = int(pxl_x)
        points[x, y, 1] = int(pxl_y)
    return points


def draw(board, triangle=False, distance=50, diameter=15, last_move=''):
    screen_width = 150 + distance * board.shape[0]
    screen_height = int(150 + math.cos(math.pi / 12) * distance * (board.shape[1] - 1) * 2)
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((125, 159, 115))

    y_pos = 75 + math.cos(math.pi / 12) * distance * (board.shape[1] - 1) / 2 if triangle else 75
    positions = matrix_to_points(board, distance, (screen_width / 2, y_pos))

    for x, y in np.ndindex(board.shape):
        if triangle and x + y >= board.shape[0]: continue

        colour = (18, 78, 138) if board[x, y] == 1 else (0, 0, 0)
        size = diameter if board[x, y] == 1 else int(diameter / 1.5)
        if "({0}, {1})".format(x, y) in last_move:
            size = int(size * 1.3)
        pxl_x = positions[x, y, 0]
        pxl_y = positions[x, y, 1]
        pygame.draw.circle(screen, colour, (pxl_x, pxl_y), size)
    pygame.display.flip()
