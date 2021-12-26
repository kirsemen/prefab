import pygame
import random
from class_and_def import *
from const import *
import numpy as np

pygame.init()

pygame.display.set_caption("Змейка")
timer = pygame.time.Clock()
courier = pygame.font.SysFont("courier", 36)

snake_blocks = np.array([SnakeBlock(COUNT_BLOCK // 2, COUNT_BLOCK // 2, SIZE_SNAKE_BLOCK, SIZE_SNAKE_BLOCK, 2)])
apple1 = np.array([])
r, g, b = 255, 255, 255

snake_blocks = snake_add(100, snake_blocks)
apple1 = apple_add(1000, apple1, snake_blocks)

gr, gg, gb = 3, 3, 3

buf_row = 0
buf_col = 1
total = 0
speed = 1
exsid = False

while True:
    screen = pygame.display.set_mode(size)
    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, BLACK, [0, HEADER_MARGING, size[0], size[1] - 70], 24)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGING])

    a = events()
    if a == True:
        exsid = True
    elif a != None:
        buf_row, buf_col = a[0], a[1]

    change(screen, courier, total, speed)

    head = snake_blocks[-1]

    new_x, new_y, new_width, new_height = get_blue_line(snake_blocks, head)
    blue_line = SnakeBlock(new_x, new_y, new_width, new_height, snake_blocks[-1].route)

    if not head.is_inside():
        print("crash")
        exsid = True

    if eatting(apple1, head) != None:
        bol, i = eatting(apple1, head)
        total += 1
        speed = total * 2 + 1
        snake_add(10, snake_blocks)
        apple1[i] = get_random_empty_block(snake_blocks)

    d_row = buf_row
    d_col = buf_col
    route = 0

    if d_row == -1:
        route = 1
    elif d_col == 1:
        route = 2
    elif d_row == 1:
        route = 3

    bol = is_triger(snake_blocks, blue_line)
    if bol != None:
        exsid = True

    r, g, b, gr, gg, gb = controle_color(r, g, b, gr, gg, gb)

    drawwing(screen, apple1, snake_blocks, blue_line, (r, g, b))

    new_head = SnakeBlock(head.x + d_row, head.y + d_col, SIZE_SNAKE_BLOCK, SIZE_SNAKE_BLOCK, route)
    snake_blocks = np.concatenate((snake_blocks, np.array([new_head])))

    snake_blocks = np.delete(snake_blocks, [0])

    if exsid == True:
        pygame.quit()
        break
    print(timer.get_fps())
    pygame.display.flip()
    timer.tick(100 + speed)
