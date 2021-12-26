from prefab.test1.rendering_2d.subsidiary_function import *


def no_smoothing_and_join(x, y, _id):
    _round = []
    if _id == 1 or _id == 4:
        _round = [2, 3]
    elif _id == 2 or _id == 3:
        _round = [1, 4]
    air_block = get_air_block(x, y, _id)
    if _id == 1:
        if not [x - 1, y] in air_block:
            _round.remove(3)
        if not [x, y - 1] in air_block:
            _round.remove(2)
    elif _id == 2:
        if not [x, y - 1] in air_block:
            _round.remove(1)
        if not [x + 1, y] in air_block:
            _round.remove(4)
    elif _id == 3:
        if not [x - 1, y] in air_block:
            _round.remove(1)
        if not [x, y + 1] in air_block:
            _round.remove(4)
    elif _id == 4:
        if not [x + 1, y] in air_block:
            _round.remove(2)
        if not [x, y + 1] in air_block:
            _round.remove(3)

    lines = []
    for id1 in _round:
        lines.append([get_pos(x, y, id1), get_pos(x, y, _id)])

    return lines
