import pygame
import random
from datetime import datetime
from datetime import timedelta

size = [400, 400]
exsid = False
speed_sloow = False
size_block = 50
marging = [(size[0] - ((size[0] - 2) // (size_block + 1) * (size_block + 1) + 1) + 3) // 2,
           (size[1] - ((size[1] - 2) // (size_block + 1) * (size_block + 1) + 1) + 3) // 2]


def get_help(texts):
    s = pygame.Surface(size, pygame.SRCALPHA)
    for i in range(len(texts)):
        courier = pygame.font.SysFont(None, 20)
        text = courier.render(texts[i], True, (255, 200, 255))
        s.blit(text,
               [size[0] - text.get_width() * (i + 1) - marging[0], size[1] - text.get_height() * (i + 1) - marging[1]])
    return s


def get_a():
    a = pygame.Surface(size, pygame.SRCALPHA)

    courier = pygame.font.SysFont(None, 100)
    text = courier.render("You win", True, (255, 0, 0))
    a.blit(text, [size[0] / 2 - text.get_width() / 2, size[1] / 2 - text.get_height() / 2])
    return a


def get_aa(laberint):
    aa = pygame.Surface(size, pygame.SRCALPHA)
    for row in range(len(laberint)):
        for col in range(len(laberint[row])):
            surf = pygame.Surface((1, size_block))

            if (laberint[row][col].left == 0 or laberint[row][col].left == None):
                surf.fill((0, 0, 0))
            else:
                surf.fill((200, 70, 0))
            aa.blit(surf, [laberint[row][col].pos[0] - 1, laberint[row][col].pos[1]])
            surf = pygame.Surface((size_block, 1))

            if (laberint[row][col].top == 0 or laberint[row][col].top == None):
                surf.fill((0, 0, 0))
            else:
                surf.fill((200, 70, 0))

            aa.blit(surf, [laberint[row][col].pos[0], laberint[row][col].pos[1] - 1])
            surf = pygame.Surface((1, size_block))

            if (laberint[row][col].right == 0 or laberint[row][col].right == None):
                surf.fill((0, 0, 0))
            else:
                surf.fill((200, 70, 0))

            aa.blit(surf, [laberint[row][col].pos[0] + size_block, laberint[row][col].pos[1]])
            surf = pygame.Surface((size_block, 1))

            if (laberint[row][col].bottom == 0 or laberint[row][col].bottom == None):
                surf.fill((0, 0, 0))
            else:
                surf.fill((200, 70, 0))

            aa.blit(surf, [laberint[row][col].pos[0], laberint[row][col].pos[1] + size_block])
    return aa


def get_aaa(laberint, pos=None):
    aaa = pygame.Surface(size, pygame.SRCALPHA)
    for row in range((size[1] - 2) // (size_block + 1)):
        for col in range((size[0] - 2) // (size_block + 1)):
            surf = pygame.Surface((size_block, size_block))
            if pos != None:
                if pos[0] == col and pos[1] == row:
                    surf.fill((200, 200, 200))
                elif laberint[row][col].open_cell == 1:
                    surf.fill((200, 70, 0))
                else:
                    surf.fill((100, 100, 100))
            else:
                if laberint[row][col].open_cell == 1:
                    surf.fill((200, 70, 0))
                else:
                    surf.fill((100, 100, 100))
            laberint[row][col].pos = [marging[0] + col * (size_block + 1), marging[1] + row * (size_block + 1)]
            aaa.blit(surf, (marging[0] + col * (size_block + 1), marging[1] + row * (size_block + 1)))
    return aaa


class snakes:
    def __init__(self, pos, laberint, plaer=False):
        self.pos = pos
        self.start_pos = pos
        self.plaer = plaer
        self.cells_end = {}
        self.laberint = laberint
        if self.plaer == False:
            self.snakes_blok = [pos]
            self.open_cell("None")

    def get_blit(self):
        win = pygame.Surface(size, pygame.SRCALPHA)
        if self.plaer == False:
            for pos in self.snakes_blok:
                pygame.draw.circle(win, (255, 255, 255),
                                   [marging[0] + size_block / 2 + pos[0] * (size_block + 1),
                                    marging[1] + size_block / 2 + pos[1] * (size_block + 1)],
                                   size_block / 2)

        pygame.draw.circle(win, (30, 30, 255),
                           [marging[0] + size_block / 2 + self.pos[0] * (size_block + 1),
                            marging[1] + size_block / 2 + self.pos[1] * (size_block + 1)],
                           size_block / 2)
        return win

    def get_rotate(self):
        arrey = []
        if self.laberint[self.pos[1]][self.pos[0]].left != None:
            if self.laberint[self.pos[1]][self.pos[0] - 1].open_cell == 0:
                arrey.append(0)
        if self.laberint[self.pos[1]][self.pos[0]].top != None:
            if self.laberint[self.pos[1] - 1][self.pos[0]].open_cell == 0:
                arrey.append(1)
        if self.laberint[self.pos[1]][self.pos[0]].right != None:
            if self.laberint[self.pos[1]][self.pos[0] + 1].open_cell == 0:
                arrey.append(2)
        if self.laberint[self.pos[1]][self.pos[0]].bottom != None:
            if self.laberint[self.pos[1] + 1][self.pos[0]].open_cell == 0:
                arrey.append(3)
        return arrey

    def open_cell(self, string):
        cell = self.laberint[self.pos[1]][self.pos[0]]
        cell.open_cell = 1
        self.cells_end[len(self.snakes_blok)] = self.pos
        if string == "go_bottom":
            cell.top = 1
            old_cell = self.laberint[self.pos[1] - 1][self.pos[0]]
            old_cell.bottom = 1
        elif string == "go_left":
            cell.right = 1
            old_cell = self.laberint[self.pos[1]][self.pos[0] + 1]
            old_cell.left = 1
        elif string == "go_top":
            cell.bottom = 1
            old_cell = self.laberint[self.pos[1] + 1][self.pos[0]]
            old_cell.top = 1
        elif string == "go_right":
            cell.left = 1
            old_cell = self.laberint[self.pos[1]][self.pos[0] - 1]
            old_cell.right = 1

    def go_right(self):
        if self.pos[0] + 1 < (size[0] - 2) // (size_block + 1):
            if self.plaer == False:
                self.snakes_blok.append(self.pos)
                self.pos = [self.pos[0] + 1, self.pos[1]]
                self.open_cell("go_right")
            else:
                cell = self.laberint[self.pos[1]][self.pos[0]]
                if cell.right == 1:
                    self.pos = [self.pos[0] + 1, self.pos[1]]

    def go_left(self):
        if self.pos[0] > 0:
            if self.plaer == False:
                self.snakes_blok.append(self.pos)
                self.pos = [self.pos[0] - 1, self.pos[1]]
                self.open_cell("go_left")
            else:
                cell = self.laberint[self.pos[1]][self.pos[0]]
                if cell.left == 1:
                    self.pos = [self.pos[0] - 1, self.pos[1]]

    def go_top(self):
        if self.pos[1] > 0:
            if self.plaer == False:
                self.snakes_blok.append(self.pos)
                self.pos = [self.pos[0], self.pos[1] - 1]
                self.open_cell("go_top")
            else:
                cell = self.laberint[self.pos[1]][self.pos[0]]
                if cell.top == 1:
                    self.pos = [self.pos[0], self.pos[1] - 1]

    def go_bottom(self):
        if self.pos[1] + 1 < (size[1] - 2) // (size_block + 1):
            if self.plaer == False:
                self.snakes_blok.append(self.pos)
                self.pos = [self.pos[0], self.pos[1] + 1]
                self.open_cell("go_bottom")
            else:
                cell = self.laberint[self.pos[1]][self.pos[0]]
                if cell.bottom == 1:
                    self.pos = [self.pos[0], self.pos[1] + 1]

    def go_beck(self):
        if len(self.snakes_blok) > 0:
            self.pos = self.snakes_blok[-1]
            self.snakes_blok.pop()


class cell:
    def __init__(self, left, top, right, bottom, open_cell, pos):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.open_cell = open_cell
        self.pos = pos

    def __str__(self):
        return f"<{self.left, self.top, self.right, self.bottom, self.open_cell, self.pos}>"

    def __repr__(self):
        return f"<{self.left, self.top, self.right, self.bottom, self.open_cell, self.pos}>"


pygame.init()
pygame.display.set_caption("Лаберинт")
timer = pygame.time.Clock()

laberint = []
aaa = pygame.Surface(size, pygame.SRCALPHA)
aa = pygame.Surface(size, pygame.SRCALPHA)


def get_laberint():
    posishn = [random.randint(0, (size[0] - 2) // (size_block + 1) - 1),
               random.randint(0, (size[1] - 2) // (size_block + 1) - 1)]
    laberint = [[cell(0, 0, 0, 0, 0, []) for i in range((size[0] - 2) // (size_block + 1))] for j in
                range((size[1] - 2) // (size_block + 1))]
    aaa = get_aaa(laberint)
    aa = get_aa(laberint)
    exsid = False
    for i in range(len(laberint)):
        for j in range(len(laberint[i])):
            if i == 0:
                laberint[i][j].top = None
            if i == len(laberint) - 1:
                laberint[i][j].bottom = None
            if j == 0:
                laberint[i][j].left = None
            if j == len(laberint[i]) - 1:
                laberint[i][j].right = None
    snake = snakes(posishn, laberint)
    x = True
    while x:
        if speed_sloow == True:
            screen = pygame.display.set_mode(size)
            screen.fill((0, 255, 100))
        number = 0
        if len(snake.get_rotate()) - 1 < 0:
            number = -1
        else:
            number = snake.get_rotate()[random.randint(0, len(snake.get_rotate()) - 1)]

        if number == 0:
            snake.go_left()
        elif number == 2:
            snake.go_right()
        elif number == 1:
            snake.go_top()
        elif number == 3:
            snake.go_bottom()
        elif number == -1:
            snake.go_beck()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exsid = True
        if speed_sloow == True:
            aaa = get_aaa(laberint)
            aa = get_aa(laberint)

        for i in [1]:
            ex = True
            for i in range(len(laberint)):
                for j in range(len(laberint[i])):
                    if laberint[i][j].open_cell == 0:
                        ex = False
            if ex == True:
                x = False

        if exsid == True:
            x = False
        if speed_sloow == True:
            screen.blit(aaa, (0, 0))
            screen.blit(aa, (0, 0))
            screen.blit(snake.get_blit(), (0, 0))
            pygame.display.flip()
        timer.tick()
    return snake, exsid


snake, exsid = get_laberint()
laberint = snake.laberint
posishn = snake.start_pos

plaer = snakes(posishn, laberint, plaer=True)
aw = [*snake.cells_end.keys()]
pos = snake.cells_end[aw[-1]]

aaa = get_aaa(laberint, pos=pos)
aa = get_aa(laberint)
a = get_a()
s = get_help(texts=["i - info"])
q = get_help(texts=["r - reset lvl"])
time2 = datetime.now() - timedelta(hours=1)
rotate = [False, False, False, False]
while True:
    screen = pygame.display.set_mode(size)
    screen.fill((0, 255, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exsid = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rotate[0] = True
            elif event.key == pygame.K_RIGHT:
                rotate[2] = True
            elif event.key == pygame.K_UP:
                rotate[1] = True
            elif event.key == pygame.K_DOWN:
                rotate[3] = True
            if event.key == pygame.K_r:
                plaer.pos = plaer.start_pos
            if event.key == pygame.K_i:
                time2 = datetime.now()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                rotate[0] = False
            elif event.key == pygame.K_RIGHT:
                rotate[2] = False
            elif event.key == pygame.K_UP:
                rotate[1] = False
            elif event.key == pygame.K_DOWN:
                rotate[3] = False
    for i in range(4):
        if i == 0 and rotate[i] == True:
            plaer.go_left()
        elif i == 1 and rotate[i] == True:
            plaer.go_top()
        elif i == 2 and rotate[i] == True:
            plaer.go_right()
        elif i == 3 and rotate[i] == True:
            plaer.go_bottom()

    if exsid == True:
        pygame.quit()
        break

    if plaer.pos == pos:
        marging = [(size[0] - ((size[0] - 2) // (size_block + 1) * (size_block + 1) + 1) + 3) // 2,
                   (size[1] - ((size[1] - 2) // (size_block + 1) * (size_block + 1) + 1) + 3) // 2]
        a = get_a()
        screen.blit(a, (0, 0))

        pygame.display.flip()

        if size[0] < 700:
            size = [size[0] + 100, size[1]]
        elif size[1] < 700:
            size = [size[0], size[1] + 100]
        elif size_block > 10:
            size_block -= 5

        if speed_sloow == True:
            pygame.time.wait(3000)
            snake, exsid = get_laberint()
        else:
            time1 = datetime.now()
            snake, exsid = get_laberint()
            time1 = int(str(datetime.now() - time1)[0:1]) * 3600 + int(str(datetime.now() - time1)[2:4]) * 60 + int(
                str(datetime.now() - time1)[5:7])
            pygame.time.wait((3 - time1) * 1000)
        plaer.pos = snake.start_pos
        plaer.laberint = snake.laberint
        laberint = snake.laberint

        aw = [*snake.cells_end.keys()]
        pos = snake.cells_end[aw[-1]]
        aaa = get_aaa(laberint, pos=pos)

        s = get_help(texts=["i - info"])
        q = get_help(texts=["r - reset lvl"])
        aa = get_aa(laberint)
        rotate = [False, False, False, False]
    screen.blit(aaa, (0, 0))
    screen.blit(aa, (0, 0))
    screen.blit(plaer.get_blit(), (0, 0))
    time3 = int(str(datetime.now() - time2)[0:1]) * 3600 + int(str(datetime.now() - time2)[2:4]) * 60 + int(
        str(datetime.now() - time2)[5:7])
    if time3 < 3:
        screen.blit(q, (0, 0))
    else:
        screen.blit(s, (0, 0))
    pygame.display.flip()
    timer.tick(6)
