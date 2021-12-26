# import pygame
# import sys
# import random
# import numpy as np
# import numba
#
#
# @numba.njit(parallel=True)
# def update(_array, _speed, _fr, _mg, _r_fr):
#     cash = _array.copy()
#     for _n in range(cash.shape[0]):
#         rx = cash[:, 0] - cash[_n, 0]
#         ry = cash[:, 1] - cash[_n, 1]
#         r = (rx ** 2 + ry ** 2 + _mg) ** 1.5
#
#         near = r <= _r_fr * min(max(cash[_n, 4], 1), 20)
#         n_near = np.sum(near)
#         if n_near >1:
#             _array[_n, 2] = (np.sum(cash[near, 2]) / n_near * _fr + cash[_n, 2]) / (_fr + 1)
#             _array[_n, 3] = (np.sum(cash[near, 3]) / n_near * _fr + cash[_n, 3]) / (_fr + 1)
#
#
#         _array[_n, 0] -= cash[_n, 2] * _speed / cash[_n, 4]
#         _array[_n, 1] -= cash[_n, 3] * _speed / cash[_n, 4]
#         _array[_n, 2] -= np.sum(rx / r * cash[:, 4]) * _speed
#         _array[_n, 3] -= np.sum(ry / r * cash[:, 4]) * _speed
#
#
#
# n_dots = 1000
# speed = 5  # 0.1 скорость
# fr = 10  # 0.025 коефецент передачи ускарения от одного объекта к другому
# mg = 6 ** 2  # 6**2 минимальный радиус
# r_fr = 10 ** 3  # 10**3 радиус объекта
# size = [1000, 500]
#
# array = []
#
# random.seed(1)
#
# for i in range(n_dots):
#     array.append([random.randint(0, size[0]),
#                   random.randint(0, size[1]),
#                   0,
#                   0,
#                   random.uniform(1, 0.1)])
#
# array = np.array(array, dtype=np.float32)
#
#
#
# pygame.init()
# screen = pygame.display.set_mode(size)
# clock = pygame.time.Clock()
#
# while True:
#     screen.fill([0, 0, 0])
#     pygame.display.set_caption(str(clock.get_fps()))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#
#     update(array, speed, fr, mg, r_fr)
#
#     for n in range(array.shape[0]):
#         pygame.draw.circle(screen, [255, 255, 255], [array[n, 0], array[n, 1]],
#                            min(max(array[n, 4], 1), 20))
#     pygame.display.update()
#     clock.tick(60)
import pygame
import sys
import random
import numpy as np
import numba


@numba.njit(parallel=True)
def update(_array, _speed):
    cash = _array.copy()
    for _n in range(cash.shape[0]):
        rx = cash[:, 0] - cash[_n, 0]
        ry = cash[:, 1] - cash[_n, 1]
        r = (rx ** 2 + ry ** 2) ** 0.51

        is_it = r == 0

        near = r < 1.5
        r[near] = 1.5
        f = cash[:, 4] * cash[_n, 4] / r ** 2
        f[is_it] = 0

        _array[_n, 2] += np.sum(np.sin(np.arctan2(rx, ry)) * f) * _speed / cash[_n, 4]
        _array[_n, 3] += np.sum(np.cos(np.arctan2(rx, ry)) * f) * _speed / cash[_n, 4]

        _array[_n, 0] += cash[_n, 2] * _speed
        _array[_n, 1] += cash[_n, 3] * _speed


n_dots = 1000
speed = 2  # 0.1 скорость
size = [1000, 500]

array = []

random.seed(1)

for i in range(n_dots):
    array.append([random.randint(0, size[0]),
                  random.randint(0, size[1]),
                  0,
                  0,
                  random.uniform(1, 10)])

for i in range(5):
    array.append([random.randint(0, size[0]),
                  random.randint(0, size[1]),
                  0,
                  0,
                  400])
array = np.array(array, dtype=np.float32)

# array = np.array([[400, 250, -0.0017, -0.0999, 1], [600, 250, 0.0017, 0.0999, 1]], dtype=np.float32)
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:
    screen.fill([0, 0, 0])
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    update(array, speed)

    for n in range(array.shape[0]):
        pygame.draw.circle(screen, [255, 255, 255], [array[n, 0], array[n, 1]],
                           min(max(array[n, 4]/4, 1), 10))

    pygame.display.update()
    clock.tick(60)
