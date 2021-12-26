from blocks import Block
from datetime import datetime
from prefab.test1.rendering_2d.subsidiary_function import *


def aqua_update(block: Block):
    if (datetime.now()-block.cooldown).total_seconds() > block.speed_water:
        block.cooldown = datetime.now()
        x = block.x
        y = block.y
        air_block = get_air_block_1(x, y)
        if [x, y+1] in air_block:
            blocks[x][y+1].default()
            blocks[x][y + 1].fullness_water = block.fullness_water
            block.default()
        else:
            _round = []
            if [x-1, y] in air_block:
                _round.append([x-1, y])
            if [x+1, y] in air_block:
                _round.append([x+1, y])
            for _x, _y in _round:

                blocks[_x][_y].default()
                blocks[_x][_y].fullness_water = block.fullness_water

        block.cooldown = datetime.now()


