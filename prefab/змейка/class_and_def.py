import pygame
import random
from const import *
import numpy as np


class SnakeBlock:
    def __init__(self, x, y, size_x, size_y, route):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.route = route

    def is_inside(self):
        return 10 <= self.x < COUNT_BLOCK - 30 and 10 <= self.y < COUNT_BLOCK - 30

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(screen, color, row, column, SIZE_ONE_BLOCK_X, SIZE_ONE_BLOCK_Y):
    pygame.draw.ellipse(screen, color, [1 + column,
                                        HEADER_MARGING + 1 + row,
                                        SIZE_ONE_BLOCK_X,
                                        SIZE_ONE_BLOCK_Y])


def get_random_empty_block(snake_blocks):
    size = random.randint(MIN_SIZE_APPLE_BLOCK, MAX_SIZE_APPLE_BLOCK)
    x = random.randint(20, COUNT_BLOCK - size - 15)
    y = random.randint(20, COUNT_BLOCK - size - 15)
    empty_block = SnakeBlock(x, y, size, size, 2)
    while True:
        size = random.randint(MIN_SIZE_APPLE_BLOCK, MAX_SIZE_APPLE_BLOCK)
        x = random.randint(20, COUNT_BLOCK - size - 15)
        y = random.randint(20, COUNT_BLOCK - size - 15)
        empty_block = SnakeBlock(x, y, size, size, 2)
        if in_blocks(empty_block, snake_blocks):
            break
    return empty_block


def snake_add(num_i, snake_blocks):
    for i in range(num_i):
        snake_blocks = np.concatenate((np.array([SnakeBlock(snake_blocks[0].x,
                                                            snake_blocks[0].y,
                                                            SIZE_SNAKE_BLOCK,
                                                            SIZE_SNAKE_BLOCK,
                                                            snake_blocks[0].route)]),
                                       snake_blocks))
    return snake_blocks


def apple_add(num_i, apple1, snake_blocks):
    i = 0
    while i < num_i:
        apple1 = np.concatenate((apple1, np.array([get_random_empty_block(snake_blocks)])))
        i += 1
    return apple1


def change(screen, courier, total, speed):
    text_total = courier.render("Total: " + str(total), 0, WIDHT)
    text_speed = courier.render("Speed: " + str(speed), 0, WIDHT)
    screen.blit(text_total, [20, 20])
    screen.blit(text_speed, [250, 20])


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("exit")
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w != 0:
                buf_row = -1
                buf_col = 0
                return [buf_row, buf_col]
            elif event.key == pygame.K_s != 0:
                buf_row = 1
                buf_col = 0
                return [buf_row, buf_col]
            elif event.key == pygame.K_a != 0:
                buf_row = 0
                buf_col = -1
                return [buf_row, buf_col]
            elif event.key == pygame.K_d != 0:
                buf_row = 0
                buf_col = 1
                return [buf_row, buf_col]
            else:
                return None


def get_blue_line(snake_blocks, head):
    if head.route == 0:
        new_x = head.x
        new_y = head.y
        new_height = head.size_x
        new_width = 2
    elif head.route == 1:
        new_x = head.x
        new_y = head.y
        new_width = head.size_y
        new_height = 2
    elif head.route == 2:
        new_x = head.x
        new_y = head.y + head.size_y
        new_width = 2
        new_height = head.size_y
    elif head.route == 3:
        new_x = head.x + head.size_x
        new_y = head.y
        new_width = head.size_y
        new_height = 2
    return new_x, new_y, new_width, new_height


def drawwing(screen, apple1, snake_blocks, blue_line, COLOR_OF_CENTER_SNAKE):
    for apple in apple1:
        draw_block(screen, RED, apple.x, apple.y, apple.size_x, apple.size_y)

    for i in range(len(snake_blocks)):
        if i >= len(snake_blocks) - 1:
            SNAKE_COLOR = SNAKE_COLOR_3
        elif (len(snake_blocks) - i) % 32 in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
            SNAKE_COLOR = SNAKE_COLOR_1
        else:
            SNAKE_COLOR = SNAKE_COLOR_2
        block = snake_blocks[i]
        draw_block(screen, SNAKE_COLOR, block.x, block.y, SIZE_SNAKE_BLOCK, SIZE_SNAKE_BLOCK)
    for block in snake_blocks:
        draw_block(screen, COLOR_OF_CENTER_SNAKE, block.x + SIZE_SNAKE_BLOCK // 2, block.y + SIZE_SNAKE_BLOCK // 2, 1,
                   1)

    if blue_line.route == 0:

        pygame.draw.arc(screen, BlUE, [1 + snake_blocks[-1].y,
                                       HEADER_MARGING + 1 + snake_blocks[-1].x,
                                       snake_blocks[-1].size_x,
                                       snake_blocks[-1].size_y], PI / 2 + 0.525, PI * 1.5 - 0.5, 2)
    elif blue_line.route == 1:
        pygame.draw.arc(screen, BlUE, [1 + snake_blocks[-1].y,
                                       HEADER_MARGING + 1 + snake_blocks[-1].x,
                                       snake_blocks[-1].size_x,
                                       snake_blocks[-1].size_y], 0 + 0.525, PI - 0.5, 2)
    elif blue_line.route == 2:
        pygame.draw.arc(screen, BlUE, [1 + snake_blocks[-1].y,
                                       HEADER_MARGING + 1 + snake_blocks[-1].x,
                                       snake_blocks[-1].size_x,
                                       snake_blocks[-1].size_y], PI * 1.5 + 0.525, PI / 2 - 0.5, 2)
    elif blue_line.route == 3:
        pygame.draw.arc(screen, BlUE, [1 + snake_blocks[-1].y,
                                       HEADER_MARGING + 1 + snake_blocks[-1].x,
                                       snake_blocks[-1].size_x,
                                       snake_blocks[-1].size_y], PI + 0.525, 0 - 0.5, 2)


def eatting(apple1, head):
    for i in range(len(apple1)):
        if (apple1[i].x - SIZE_SNAKE_BLOCK + 1 <= head.x
                <= apple1[i].x + apple1[i].size_x - 1 and
                apple1[i].y - SIZE_SNAKE_BLOCK + 1 <= head.y
                <= apple1[i].y + apple1[i].size_y - 1):
            return True, i


def is_triger(snake_blocks, blue_line):
    for snake_block in snake_blocks:
        if (((blue_line.route == 0 or blue_line.route == 2) and
             snake_block.y + SIZE_SNAKE_BLOCK - SIZE_COLAUDER_SNAKE_BLOCK[1]
             >= blue_line.y + 1 >
             snake_block.y + SIZE_COLAUDER_SNAKE_BLOCK[1]
             and
             snake_block.x + SIZE_SNAKE_BLOCK - 1 - SIZE_COLAUDER_SNAKE_BLOCK[0]
             >= blue_line.x >=
             snake_block.x - SIZE_SNAKE_BLOCK + 1 + SIZE_COLAUDER_SNAKE_BLOCK[0]
             and snake_block != snake_blocks[-1] and snake_block != snake_blocks[-2])
                or
                ((blue_line.route == 1 or blue_line.route == 3) and
                 snake_block.y + SIZE_SNAKE_BLOCK - 1 - SIZE_COLAUDER_SNAKE_BLOCK[0]
                 >= blue_line.y >=
                 snake_block.y - SIZE_SNAKE_BLOCK + 1 + SIZE_COLAUDER_SNAKE_BLOCK[0]
                 and
                 snake_block.x + SIZE_SNAKE_BLOCK - SIZE_COLAUDER_SNAKE_BLOCK[1]
                 >= blue_line.x + 1 >
                 snake_block.x + SIZE_COLAUDER_SNAKE_BLOCK[1]
                 and snake_block != snake_blocks[-1] and snake_block != snake_blocks[-2])):
            return True


def in_blocks(empty_block, blocks):
    for block in blocks:
        if (empty_block.x - block.size_x + 1 <= block.x
                <= empty_block.x + empty_block.size_x - 1 and
                empty_block.y - block.size_y + 1 <= block.y
                <= empty_block.y + empty_block.size_y - 1):
            return False
    return True


def controle_color(r, g, b, gr, gg, gb):
    number = random.randint(1, 3)
    if number == 1:
        r += gr
    elif number == 2:
        g += gg
    else:
        b += gb

    if r >= 255 or r <= 0:
        gr = -gr
    elif g >= 255 or g <= 0:
        gg = -gg
    elif b >= 255 or b <= 0:
        gb = -gb

    if r >= 255:
        r = 255
    if r <= 0:
        r = 0
    if g >= 255:
        g = 255
    if g <= 0:
        g = 0
    if b >= 255:
        b = 255
    if b <= 0:
        b = 0
    return r, g, b, gr, gg, gb
