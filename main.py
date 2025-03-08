import pygame as pg
from settings import *
import numpy as np
import time

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Le Jeu De La Vie")
clock = pg.time.Clock()
running = True
paused = False

cell_map = np.zeros((ROWS, COLS), dtype=np.int8)

def rendering():
    for y in range(cell_map.shape[0]):
        for x in range(cell_map.shape[1]):
            if cell_map[y, x] == 1:
                pg.draw.rect(surface=screen, color=WHITE, rect=(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pg.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=1)


def count_neighbours(x, y):
    alive = 0
    for y_cor in range(y-1, y+2):
        for x_cor in range(x-1, x+2):
            if 0 <= y_cor < ROWS and 0 <= x_cor < COLS and (x_cor, y_cor) != (x, y):
                if cell_map[y_cor, x_cor] == 1:
                    alive += 1
    
    return alive


def update():
    global cell_map
    
    new_board = np.zeros((ROWS, COLS), dtype=np.int8)
    for y in range(cell_map.shape[0]):
        for x in range(cell_map.shape[1]):
            neigbours = count_neighbours(x, y)
            if cell_map[y, x] == 1:
                if neigbours < 2:
                    new_board[y, x] = 0
                elif 2 <= neigbours <= 3:
                    new_board[y, x] = 1
            elif cell_map[y, x] == 0:
                if neigbours == 3:
                    new_board[y, x] = 1

    cell_map = new_board

def draw(x, y, mode):
    global cell_map

    new_board = cell_map

    if mode == 0:
        new_board[y, x] = 1
    else:
        new_board[y, x] = 0

    cell_map = new_board


while running:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
            elif event.key == pg.K_SPACE:
                paused = not paused
        if event.type == pg.MOUSEBUTTONDOWN:
            mode = 0
            if event.button == 0:
                mode = 0
            elif event.button == 3:
                mode = 1
            mouse_x, mouse_y = pg.mouse.get_pos()
            draw(mouse_x//CELL_SIZE, mouse_y//CELL_SIZE, mode)


    if not paused:
        update()

    screen.fill(BG_COLOR)
    rendering()

    pg.display.flip()

    clock.tick(FPS)

pg.quit()