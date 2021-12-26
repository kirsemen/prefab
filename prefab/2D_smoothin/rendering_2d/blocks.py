from config import *
from datetime import datetime


class Block:
    def __init__(self, x, y):
        self.is_not_air = False
        self.is_loose = False
        self.fullness_water = 0
        self.speed_water = 1
        self.cooldown = datetime.now()
        self.x = x
        self.y = y
        self.default()

    def default(self):
        self.is_not_air = False
        self.is_loose = False
        self.fullness_water = 0
        self.cooldown = datetime.now()

    def __str__(self):
        return f"is_not_air: {self.is_not_air}, is_loose: {self.is_loose}, " \
               f"x: {self.x}, y: {self.y}, fullness_water: {self.fullness_water}"


blocks = [[Block(x, y) for y in range(int(size[1] / size_block) - 2)]
          for x in range(int(size[0] / size_block) - 2)]
