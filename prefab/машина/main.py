import pygame
import sys
import math
import numba

pygame.init()
size = [800, 650]
font = pygame.font.Font(None, 36)

points = [(238, 112), (126, 46), (167, 195), (45, 168), (162, 298), (45, 320), (176, 391), (58, 454), (200, 475),
          (106, 531), (257, 499), (205, 588), (315, 508), (328, 604), (401, 508), (439, 613), (488, 494), (546, 603),
          (565, 433), (666, 521), (629, 391), (714, 449), (683, 334), (742, 358), (677, 269), (753, 286), (682, 209),
          (755, 199), (666, 159), (736, 116), (623, 121), (660, 45), (589, 99), (594, 27), (532, 95), (497, 8),
          (481, 87), (445, 7), (436, 83), (380, 2), (351, 81), (314, 2), (284, 87), (207, 3), (238, 112), (126, 46)]


def level():
    _surf = pygame.Surface(size)
    _surf.set_colorkey((0, 0, 0))
    last = []
    for f, s in zip(points[::2], points[1::2]):
        if len(last) >= 2:
            pygame.draw.polygon(_surf, (150, 150, 150), [*last, s, f])
        last = [f, s]
    return _surf


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_arr(self):
        return [self.x, self.y]

    def __repr__(self):
        return f"{self.x}, {self.y}"


class Vector(Pos):
    pass


@numba.jit(nopython=True, parallel=True)
def collide(pos) -> bool:
    b = False
    last = []

    for f, s in zip(points[::2], points[1::2]):
        if len(last) >= 2:
            if in_quadrilateral(pos, f, s, *last):
                b = True
                break
        last = [f, s]
    return b


@numba.jit(nopython=True, parallel=True)
def in_quadrilateral(point: list, t1: list, t2: list, t3: list, t4: list) -> bool:
    return in_triangle(point, t1, t2, t3) or in_triangle(point, t2, t3, t4)


@numba.jit(nopython=True, parallel=True)
def in_triangle(point: list, t1: list, t2: list, t3: list) -> bool:
    [xa, ya] = t1
    [xb, yb] = t2
    [xc, yc] = t3
    [xd, yd] = point
    return (((xd - xa) * (yb - ya) - (yd - ya) * (xb - xa)) *
            ((xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)) >= 0) and \
           (((xd - xb) * (yc - yb) - (yd - yb) * (xc - xb)) *
            ((xa - xb) * (yc - yb) - (ya - yb) * (xc - xb)) >= 0) and \
           (((xd - xc) * (ya - yc) - (yd - yc) * (xa - xc)) *
            ((xb - xc) * (ya - yc) - (yb - yc) * (xa - xc)) >= 0)


class Line:
    def __init__(self, angle: float, last_car_length):
        self.angle = angle
        self.last_car_length = last_car_length
        self.end_pos = Pos(0, 0)

    @staticmethod
    @numba.jit(nopython=True)
    def get_margin(angle: float):
        x = math.sin(math.radians(angle))
        y = math.cos(math.radians(angle))
        return [x * 10, y * 10]

    @staticmethod
    @numba.jit(nopython=True)
    def get_length(center: list, margin: list, rang: list, points1: [int, int]) -> float and list:
        m = 0.0
        while m < 300:
            b = False

            for i in rang:
                if i >= 2:
                    point = [margin[0] * m + center[0], margin[1] * m + center[1]]
                    t1 = points1[i * 2]
                    t2 = points1[i * 2 + 1]
                    t3 = points1[i * 2 - 1]
                    t4 = points1[i * 2 - 2]

                    xa =points1[i * 2][0]
                    ya = points1[i * 2][1]
                    xb = points1[i * 2 + 1][0]
                    yb = points1[i * 2 + 1][1]
                    xc = points1[i * 2 - 1][0]
                    yc = points1[i * 2 - 1][1]
                    xd = points1[i * 2 - 2][0]
                    yd = points1[i * 2 - 2][1]
                    xf = margin[0] * m + center[0]
                    yf = margin[1] * m + center[1]
                    c1 = (((xf - xa) * (yb - ya) - (yf - ya) * (xb - xa)) *
                        ((xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)) >= 0) and \
                        (((xf - xb) * (yc - yb) - (yf - yb) * (xc - xb)) *
                        ((xa - xb) * (yc - yb) - (ya - yb) * (xc - xb)) >= 0) and \
                        (((xf - xc) * (ya - yc) - (yf - yc) * (xa - xc)) *
                        ((xb - xc) * (ya - yc) - (yb - yc) * (xa - xc)) >= 0)

                    c2 = (((xf - xd) * (yb - yd) - (yf - yd) * (xb - xd)) *
                        ((xc - xd) * (yb - yd) - (yc - yd) * (xb - xd)) >= 0) and \
                        (((xf - xb) * (yc - yb) - (yf - yb) * (xc - xb)) *
                        ((xd - xb) * (yc - yb) - (yd - yb) * (xc - xb)) >= 0) and \
                        (((xf - xc) * (yd - yc) - (yf - yc) * (xd - xc)) *
                        ((xb - xc) * (yd - yc) - (yb - yc) * (xd - xc)) >= 0)
                    if c1 or c2:
                        b = True
                        break
            if not b:
                break
            m += 1

        return m, [margin[0] * m + center[0], margin[1] * m + center[1]]


class Axis:
    def __init__(self, point: Pos):
        self.point = point
        self.vector = Vector(0, 0)
        self.axis_angle = 0
        self.wheels_angle = 0

    def get_vector_by_meters(self, meters):
        angle = self.axis_angle + self.wheels_angle
        x = math.sin(math.radians(angle)) * meters
        y = math.cos(math.radians(angle)) * meters
        return Vector(x, y)

    def go_by_vector(self, vector: Vector):
        self.point.x += vector.x
        self.point.y -= vector.y

    def get_all_angle(self) -> float:
        return self.axis_angle + self.wheels_angle


class Car:
    def __init__(self):
        self.size = [30, 60]
        self.first_axis = Axis(Pos(310, 550))
        self.second_axis = Axis(Pos(340, 550))
        img = pygame.image.load("car.png")
        img = pygame.transform.rotate(img, 90)
        self.img = pygame.transform.scale(img, self.size)
        self.angle = 0
        self.now_speed = 0
        self.speed = 0.002
        self.max_speed = 0.5
        self.max_angle = 30
        self.end = False
        self.lines = [Line(90, 15), Line(63, 33), Line(0, 30), Line(-63, 33),
                      Line(-90, 15), Line(-117, 33), Line(180, 30), Line(117, 33)]
        self.update()

    def handle_event(self, _event):
        pass

    def update(self):
        angle = self.get_angel()
        self.angle = angle
        self.first_axis.axis_angle = angle
        self.second_axis.axis_angle = angle

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.first_axis.wheels_angle = -self.max_angle
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.first_axis.wheels_angle = self.max_angle
        else:
            self.first_axis.wheels_angle = 0

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.now_speed += self.speed

        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.now_speed -= self.speed

        self.now_speed *= 0.997

        if (keys[pygame.K_a] and not keys[pygame.K_d]) or (keys[pygame.K_d] and not keys[pygame.K_a]):
            self.now_speed *= 0.998

        if self.now_speed > self.max_speed:
            self.now_speed = self.max_speed
        elif self.now_speed < -self.max_speed * 0.5:
            self.now_speed = -self.max_speed * 0.5

        if self.now_speed > 0:
            i = 0.2
            for _ in range(int(self.now_speed // i)):
                vector1 = self.first_axis.get_vector_by_meters(i)
                self.first_axis.go_by_vector(vector1)
                vector2 = self.second_axis.get_vector_by_meters(i)
                self.second_axis.go_by_vector(vector2)

            vector1 = self.first_axis.get_vector_by_meters(self.now_speed % i)
            self.first_axis.go_by_vector(vector1)
            vector2 = self.second_axis.get_vector_by_meters(self.now_speed % i)
            self.second_axis.go_by_vector(vector2)
        else:
            i = -0.2
            for _ in range(int(self.now_speed // i)):
                vector1 = self.first_axis.get_vector_by_meters(i)
                self.first_axis.go_by_vector(vector1)
                vector2 = self.second_axis.get_vector_by_meters(i)
                self.second_axis.go_by_vector(vector2)

            vector1 = self.first_axis.get_vector_by_meters(self.now_speed % i)
            self.first_axis.go_by_vector(vector1)
            vector2 = self.second_axis.get_vector_by_meters(self.now_speed % i)
            self.second_axis.go_by_vector(vector2)

        angle = self.get_angel()
        self.angle = angle
        center = self.get_center()
        point_3 = Pos(center.x, center.y - 15)
        angle2 = (180 - angle) / 2
        angle3 = angle / 2
        a2 = math.sin(math.radians(angle3)) * 30
        b2 = math.sin(math.radians(angle2)) * 30
        pos1 = Pos(math.sin(math.radians(angle2)) * a2, math.cos(math.radians(angle2)) * a2)
        pos2 = Pos(math.sin(math.radians(angle3)) * b2, math.cos(math.radians(angle3)) * b2)
        if self.first_axis.point.x < self.second_axis.point.x:
            if angle > 0:
                pos1.x *= -1
            if angle < 0:
                pos2.x *= -1
        else:
            if angle < 0:
                pos1.x *= -1
            if angle > 0:
                pos2.x *= -1
        self.first_axis.point.x = point_3.x + pos1.x
        self.first_axis.point.y = point_3.y + pos1.y
        self.second_axis.point.x = point_3.x + pos2.x
        self.second_axis.point.y = point_3.y + pos2.y

        for line in self.lines:
            m, pos, b = line.get_length(self.get_center().get_arr(),
                                        line.get_margin(float(-self.angle + line.angle)),
                                        list(range(int(len(points) / 2))), list(points))
            if b:
                self.end = True

    def draw(self, screen):

        _surf = self.img
        _surf = pygame.transform.rotate(_surf, -self.angle)
        center = self.get_center()
        _screen.blit(_surf, _surf.get_rect(center=center.get_arr()))
        for line in self.lines:
            pygame.draw.line(screen, (40, 40, 0), center.get_arr(), line.end_pos.get_arr())

        return screen

    def get_center(self) -> Pos:
        return Pos((self.first_axis.point.x + self.second_axis.point.x) / 2,
                   (self.first_axis.point.y + self.second_axis.point.y) / 2)

    def get_angel(self) -> float:
        center = self.get_center()
        point_3 = Pos(center.x, center.y - 15)
        a = math.sqrt((point_3.x - self.second_axis.point.x) ** 2 + (point_3.y - self.second_axis.point.y) ** 2)
        b = math.sqrt((point_3.x - self.first_axis.point.x) ** 2 + (point_3.y - self.first_axis.point.y) ** 2)
        angle = 180 - math.degrees(math.atan2(a, b)) * 2

        if self.first_axis.point.x < center.x:
            angle *= -1
        return angle


car = Car()

level_surf = level()
while True:
    _screen = pygame.display.set_mode(size)
    _screen.fill((60, 160, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        car.handle_event(event)
    car.update()
    _screen.blit(level_surf, [0, 0])
    pygame.draw.line(_screen, (255, 255, 255), (329, 510), (329, 603), 40)
    _screen = car.draw(_screen)
    surf = font.render(str(int(round(car.now_speed, 3) * 400)), True, (0, 0, 0))
    _screen.blit(surf, [745, 10])

    pygame.display.flip()
