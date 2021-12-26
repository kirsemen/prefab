from config import *
from blocks import blocks


def get_block_1(x, y):
    return [[x, y - 1], [x - 1, y], [x + 1, y], [x, y + 1]]


def get_air_block_1(x, y):
    rounds = []
    for _x, _y in get_block_1(x, y):
        if 0 <= _x < len(blocks) and 0 <= _y < len(blocks[0]):
            if not blocks[_x][_y].is_not_air:
                rounds.append([_x, _y])
        else:
            rounds.append([_x, _y])
    return rounds

def get_block(x, y, _id):
    rounds = []
    if _id == 1:
        x += -1
        y += -1
    elif _id == 2:
        x += 0
        y += -1
    elif _id == 3:
        x += -1
        y += 0
    elif _id == 4:
        x += 0
        y += 0
    for n in range(4):
        i1 = 0
        j1 = 0
        if n == 0:
            i1 += 0
            j1 += 0
        elif n == 1:
            i1 += 1
            j1 += 0
        elif n == 2:
            i1 += 0
            j1 += 1
        elif n == 3:
            i1 += 1
            j1 += 1
        rounds.append([x + i1, y + j1])
    return rounds


def get_air_block(x, y, _id):
    rounds = []
    for _x, _y in get_block(x, y, _id):
        if 0 <= _x < len(blocks) and 0 <= _y < len(blocks[0]):
            if not blocks[_x][_y].is_not_air:
                rounds.append([_x, _y])
        else:
            rounds.append([_x, _y])
    return rounds


def get_loose_block(x, y, _id):
    rounds = []
    for _x, _y in get_block(x, y, _id):
        if 0 <= _x < len(blocks) and 0 <= _y < len(blocks[0]):
            if blocks[_x][_y].is_loose and blocks[_x][_y].is_not_air:
                rounds.append([_x, _y])

    return rounds


def get_pos(x, y, _id):
    if _id == 1:
        return [(x + 1) * size_block, (y + 1) * size_block]
    elif _id == 2:
        return [(x + 2) * size_block, (y + 1) * size_block]
    elif _id == 3:
        return [(x + 1) * size_block, (y + 2) * size_block]
    elif _id == 4:
        return [(x + 2) * size_block, (y + 2) * size_block]


def mean_two_point(pos1, pos2):
    return [(pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2]
