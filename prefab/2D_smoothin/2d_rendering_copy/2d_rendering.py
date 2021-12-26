from smoothing import smoothing_and_join
from config import *
from blocks import blocks

import pygame
import sys

pygame.init()

screen = pygame.display.set_mode(size)

smoothing = True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for x in range(len(blocks)):
                for y in range(len(blocks[x])):
                    if (x + 1) * size_block <= event.pos[0] <= (x + 2) * size_block and \
                            (y + 1) * size_block <= event.pos[1] <= (y + 2) * size_block:
                        if blocks[x][y].is_not_air:
                            blocks[x][y].is_not_air = blocks[x][y].default()
                        else:
                            blocks[x][y].is_not_air = True
                            blocks[x][y].is_loose = not pygame.key.get_pressed()[pygame.K_LCTRL]
    for x in range(len(blocks)):
        for y in range(len(blocks[x])):
            if blocks[x][y].is_not_air:
                color = [255, 255, 255]
                if not blocks[x][y].is_loose:
                    color = [0, 0, 255]
                pygame.draw.rect(screen, color,
                                 [(x + 1) * size_block, (y + 1) * size_block, size_block + 1, size_block + 1], 1)

    for x in range(len(blocks)):
        for y in range(len(blocks[x])):
            if blocks[x][y].is_not_air:
                if smoothing:
                    for _id in range(1, 5):
                        lines = smoothing_and_join(x, y, _id)
                        for start_pos, end_pos in lines:
                            pygame.draw.line(screen, [0, 255, 0], start_pos, end_pos)
                else:
                    pygame.draw.rect(screen, [0, 255, 0],
                                     [(x + 1) * size_block, (y + 1) * size_block,
                                      size_block, size_block],
                                     1)

    pygame.display.update()
    screen.fill((0, 0, 0))
