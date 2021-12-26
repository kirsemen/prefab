r = 4
D = ["ab", "abc", "ac", "de", "ef", "def"]
# t = open("expanded", "r").readlines(-1)
# for i in range(len(t)):
#     if i != len(t) - 1:
#         line = t[i][0:-1]
#         arg = line.split(",")
#         if arg.count("?"):
#             arg.remove("?")
#         D.append(arg)
print("end render")


class C_1:
    def __init__(self):
        self.collection = []
        self.H = 0
        self.W = 0

    def update(self):
        u = {}
        for _str in self.collection:
            for char in _str:
                if char in u:
                    u[char] += 1
                else:
                    u[char] = 1

        self.H, self.W = sum(list(u.values())) / len(list(u.keys())), len(list(u.keys()))

    @staticmethod
    def profit(H, W, _r):
        return H / W ** (_r - 1)

    @staticmethod
    def get_H_W(_collection):
        u = {}
        for _str in _collection:
            for char in _str:
                if char in u:
                    u[char] += 1
                else:
                    u[char] = 1

        return sum(list(u.values())) / len(list(u.keys())), len(list(u.keys()))

    def __str__(self):
        return f"{self.collection}"


def get_answer_1(_D, _r):
    answer = []
    _i = 1
    for i in range(len(_D)):
        if i % 10 == 0:
            print(f"терация {_i}, процес {i + 1}/{len(_D)}")
        _str = _D[i]
        if not answer:
            collection = C_1()
            collection.collection.append(_str)
            collection.update()
            answer.append(collection)
            continue

        v = []
        for collection in answer:
            v.append(C_1.profit(*collection.get_H_W(collection.collection + [_str]), _r) -
                     C_1.profit(collection.H, collection.W, _r))

        _H_1 = _H_2 = sum([C.H for C in answer])
        _W_1 = _W_2 = sum([C.W for C in answer])

        _H_1, _W_1 = C_1.get_H_W(answer[v.index(max(v))].collection + [_str])
        _H_1 += _H_1 - answer[v.index(max(v))].H
        _W_1 += _W_1 - answer[v.index(max(v))].H

        _H_2, _W_2 = C_1.get_H_W(_str)
        _H_2 += _H_2
        _W_2 += _W_2

        _H_1 /= len(answer)
        _H_2 /= len(answer)
        if C_1.profit(_H_1, _W_1, _r) <= C_1.profit(_H_2, _W_2, _r):
            collection = C_1()
            collection.collection.append(_str)
            collection.update()
            answer.append(collection)
        else:
            collection = answer[v.index(max(v))]
            collection.collection.append(_str)
            collection.update()

    for _c in answer:
        print(_c)

    _i += 1
    while True:
        last_answer = answer.copy()
        i = 0
        for k in range(len(answer)):
            _C = answer[k]
            for _str in _C.collection:
                if i % 10 == 0:
                    print(f"терация {_i}, процес {i + 1}/{len(_D)}")
                i += 1

                v = []
                for collection in answer:
                    if collection != _C:
                        v.append(C_1.profit(*collection.get_H_W(collection.collection + [_str]), _r) -
                                 C_1.profit(collection.H, collection.W, _r))
                    else:
                        v.append(0)

                if answer[v.index(max(v))] != _C:
                    _C.collection.remove(_str)
                    if not _C.collection:
                        answer.pop(k)
                    else:
                        _C.update()
                    answer[v.index(max(v))].collection.append(_str)
                    answer[v.index(max(v))].update()

        for _c in answer:
            print(_c)
        if last_answer == answer:
            print("end sort")
            break

        _i += 1

    return answer


for c in get_answer_1(D, r):
    print(c)
