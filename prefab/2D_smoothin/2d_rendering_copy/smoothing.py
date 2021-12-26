from config import *
from blocks import blocks

import math


# главные функции

def smoothing_and_join(x, y, _id):
    points = get_mean_point(x, y, _id)

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

    if not points:
        points = [get_pos(x, y, _id)]
    for id1 in _round:
        a = get_mean_point(x, y, id1)
        if not a:
            a = [get_pos(x, y, id1)]
        b = {}
        for _x, _y in points:
            for _x1, _y1 in a:
                n = math.sqrt((_x - _x1) ** 2 + (_y - _y1) ** 2)
                b[n] = [_x, _y, _x1, _y1]

        keys = list(b.keys())
        keys.sort()
        lines.append([b[keys[0]][0:2], b[keys[0]][2:4]])

    return lines


def get_mean_point(x, y, _id):
    points = [[], []]
    for _round in [-1, 1]:
        box = get_next_point(x, y, _id, _round)

        if len(box) == 3:
            x1, y1, id1 = box
            points[0].append(get_pos(x1, y1, id1))

            _box = get_next_point(x1, y1, id1, _round, x, y, _id)
            if len(_box) == 3:
                x2, y2, id2 = _box
                points[0].append(
                    mean_two_point(get_pos(x2, y2, id2), get_pos(x, y, _id)))
        elif len(box) == 2:

            for _n in range(len(box)):
                x1, y1, id1 = box[_n]
                points[_n].append(get_pos(x1, y1, id1))

                _box = get_next_point(x1, y1, id1, _round, x, y, _id)
                if len(_box) == 3:
                    x2, y2, id2 = _box
                    points[_n].append(
                        mean_two_point(get_pos(x2, y2, id2), get_pos(x, y, _id)))


    _points_ = []
    if points[0] and not points[1]:
        mean_x = 0
        mean_y = 0
        for _x, _y in points[0]:
            mean_x += _x / len(points[0])
            mean_y += _y / len(points[0])
        _points_.append(
            mean_two_point([mean_x, mean_y], get_pos(x, y, _id)))
    elif points[0] and points[1]:

        for _points in points:
            mean_x = 0
            mean_y = 0
            for _x, _y in _points:
                mean_x += _x / len(_points)
                mean_y += _y / len(_points)
            _points_.append(
                mean_two_point([mean_x, mean_y], get_pos(x, y, _id)))

    return _points_


def get_next_point(x, y, _id, _round, old_i=None, old_j=None, old_id=None):
    air_block = get_air_block(x, y, _id)
    loose_block = get_loose_block(x, y, _id)

    if len(loose_block) != 4 - len(air_block):
        return []
    if air_block:
        if _round == -1:
            if not (len(air_block) == 2 and (
                    (
                            (x - air_block[0][0] == 0 and abs(y - air_block[0][1]) == 1) or
                            (abs(x - air_block[0][0]) == 1 and y - air_block[0][1] == 0)
                    ) and
                    (
                            (x - air_block[1][0] == 0 and abs(y - air_block[1][1]) == 1) or
                            (abs(x - air_block[1][0]) == 1 and y - air_block[1][1] == 0)
                    )
            )):
                if _id == 1:
                    x += 0
                    y += 0
                elif _id == 2:
                    x += 1
                    y += 0
                elif _id == 3:
                    x += 0
                    y += 1
                elif _id == 4:
                    x += 1
                    y += 1
                if (not [x, y] in air_block) and [x - 1, y] in air_block:
                    return [x, y, 3]
                elif (not [x - 1, y] in air_block) and [x - 1, y - 1] in air_block:
                    return [x - 1, y, 1]
                elif (not [x - 1, y - 1] in air_block) and [x, y - 1] in air_block:
                    return [x - 1, y - 1, 2]
                elif (not [x, y - 1] in air_block) and [x, y] in air_block:
                    return [x, y - 1, 4]
            elif not old_i is None and \
                    not old_j is None and \
                    not old_id is None:
                if x - old_i == 0 and y - old_j == 1:
                    if old_id == 3:
                        old_id = 1
                    elif old_id == 4:
                        old_id = 2
                elif x - old_i == 1 and y - old_j == 0:
                    if old_id == 2:
                        old_id = 1
                    elif old_id == 4:
                        old_id = 3
                elif x - old_i == 0 and y - old_j == -1:
                    if old_id == 1:
                        old_id = 3
                    elif old_id == 2:
                        old_id = 4
                elif x - old_i == -1 and y - old_j == 0:
                    if old_id == 1:
                        old_id = 2
                    elif old_id == 3:
                        old_id = 4
                elif x - old_i == -1 and y - old_j == -1:
                    if old_id == 1:
                        old_id = 4
                elif x - old_i == 1 and y - old_j == 1:
                    if old_id == 4:
                        old_id = 1
                elif x - old_i == -1 and y - old_j == 1:
                    if old_id == 3:
                        old_id = 2
                elif x - old_i == 1 and y - old_j == -1:
                    if old_id == 2:
                        old_id = 3

                if old_id == 1:
                    if _id == 2:
                        return [x + 1, y - 1, old_id]
                    elif _id == 3:
                        return [x - 1, y + 1, old_id]
                elif old_id == 2:
                    if _id == 1:
                        return [x - 1, y - 1, old_id]
                    elif _id == 4:
                        return [x + 1, y + 1, old_id]
                elif old_id == 3:
                    if _id == 1:
                        return [x - 1, y - 1, old_id]
                    elif _id == 4:
                        return [x + 1, y + 1, old_id]
                elif old_id == 4:
                    if _id == 2:
                        return [x + 1, y - 1, old_id]
                    elif _id == 3:
                        return [x - 1, y + 1, old_id]

        elif _round == 1:
            if not (len(air_block) == 2 and (
                    (
                            (x - air_block[0][0] == 0 and abs(y - air_block[0][1]) == 1) or
                            (abs(x - air_block[0][0]) == 1 and y - air_block[0][1] == 0)
                    ) and
                    (
                            (x - air_block[1][0] == 0 and abs(y - air_block[1][1]) == 1) or
                            (abs(x - air_block[1][0]) == 1 and y - air_block[1][1] == 0)
                    )

            )):

                if _id == 1:
                    x -= 1
                    y += 0
                elif _id == 2:
                    x -= 0
                    y += 0
                elif _id == 3:
                    x -= 1
                    y += 1
                elif _id == 4:
                    x -= 0
                    y += 1
                if (not [x, y] in air_block) and [x + 1, y] in air_block:
                    return [x, y, 4]
                elif (not [x + 1, y] in air_block) and [x + 1, y - 1] in air_block:
                    return [x + 1, y, 2]
                elif (not [x + 1, y - 1] in air_block) and [x, y - 1] in air_block:
                    return [x + 1, y - 1, 1]
                elif (not [x, y - 1] in air_block) and [x, y] in air_block:
                    return [x, y - 1, 3]
            elif not old_i is None and \
                    not old_j is None and \
                    not old_id is None:
                if x - old_i == 0 and y - old_j == 1:
                    if old_id == 3:
                        old_id = 1
                    elif old_id == 4:
                        old_id = 2
                elif x - old_i == 1 and y - old_j == 0:
                    if old_id == 2:
                        old_id = 1
                    elif old_id == 4:
                        old_id = 3
                elif x - old_i == 0 and y - old_j == -1:
                    if old_id == 1:
                        old_id = 3
                    elif old_id == 2:
                        old_id = 4
                elif x - old_i == -1 and y - old_j == 0:
                    if old_id == 1:
                        old_id = 2
                    elif old_id == 3:
                        old_id = 4
                elif x - old_i == -1 and y - old_j == -1:
                    if old_id == 1:
                        old_id = 4
                elif x - old_i == 1 and y - old_j == 1:
                    if old_id == 4:
                        old_id = 1
                elif x - old_i == -1 and y - old_j == 1:
                    if old_id == 3:
                        old_id = 2
                elif x - old_i == 1 and y - old_j == -1:
                    if old_id == 2:
                        old_id = 3

                if old_id == 1:
                    if _id == 2:
                        return [x + 1, y - 1, old_id]
                    elif _id == 3:
                        return [x - 1, y + 1, old_id]
                elif old_id == 2:
                    if _id == 1:
                        return [x - 1, y - 1, old_id]
                    elif _id == 4:
                        return [x + 1, y + 1, old_id]
                elif old_id == 3:
                    if _id == 1:
                        return [x - 1, y - 1, old_id]
                    elif _id == 4:
                        return [x + 1, y + 1, old_id]
                elif old_id == 4:
                    if _id == 2:
                        return [x + 1, y - 1, old_id]
                    elif _id == 3:
                        return [x - 1, y + 1, old_id]

        _points = []
        for _n in range(2):
            i1, j1, id1 = 0, 0, 0
            if _id == 4:
                if _n == 0:
                    id1 = 2
                else:
                    id1 = 3

                if (_round == -1 and _n == 0) or (_round == 1 and _n == 1):
                    i1, j1 = x, y
                else:
                    i1, j1 = x + 1, y + 1
            elif _id == 3:
                if _n == 0:
                    id1 = 4
                else:
                    id1 = 1

                if (_round == -1 and _n == 0) or (_round == 1 and _n == 1):
                    i1, j1 = x, y
                else:
                    i1, j1 = x - 1, y + 1
            elif _id == 2:
                if _n == 0:
                    id1 = 4
                else:
                    id1 = 1

                if (_round == -1 and _n == 0) or (_round == 1 and _n == 1):
                    i1, j1 = x + 1, y - 1
                else:
                    i1, j1 = x, y
            elif _id == 1:
                if _n == 0:
                    id1 = 2
                else:
                    id1 = 3
                if (_round == -1 and _n == 0) or (_round == 1 and _n == 1):
                    i1, j1 = x - 1, y - 1
                else:
                    i1, j1 = x, y
            _points.append([i1, j1, id1])

        return _points
    return []


# вспомогательные функции
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
