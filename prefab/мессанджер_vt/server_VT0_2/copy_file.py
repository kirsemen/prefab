import pygame
import sys
from inspect import getsourcefile
from os.path import abspath

screen = pygame.display.set_mode([200, 200])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    try:
        path = abspath(getsourcefile(lambda:0))
        open(path)
    except:
        sys.exit()
    pygame.display.flip()