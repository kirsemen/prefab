import math
import random


class real(float):
    def __mul__(self, other):
        if other.__class__ == Vec2:
            return Vec2(self.real * other.x, self.real * other.y)
        else:
            return self.real * other


class int32(int):
    pass


PI = real(3.141592741)
EPSILON = real(0.0001)


class Vec2:
    def __init__(self, x: real, y: real):
        self.x = x
        self.y = y
        self.m = [[real(0)]]
        self.v = [real(0), real(0)]

    def set(self, x=real(0), y=real(0)):
        self.x = x
        self.y = y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __mul__(self, other):
        if other.__class__ == real:
            return Vec2(self.x * other, self.y * other)
        else:
            raise Exception("Error in math operation")

    def __truediv__(self, other):
        if other.__class__ == real:
            return Vec2(self.x / other, self.y / other)
        else:
            raise Exception("Error in math operation")

    def __imul__(self, other):
        if other.__class__ == real:
            self.x *= other
            self.y *= other
        else:
            raise Exception("Error in math operation")

    def __add__(self, other):
        if other.__class__ == Vec2:
            return Vec2(self.x + other.x, self.y + other.y)
        elif other.__class__ == real:
            return Vec2(self.x + other, self.y + other)
        else:
            raise Exception("Error in math operation")

    def __iadd__(self, other):
        if other.__class__ == Vec2:
            self.x += other.x
            self.y += other.y
        else:
            raise Exception("Error in math operation")

    def __rsub__(self, other):
        if other.__class__ == Vec2:
            return Vec2(self.x - other.x, self.y - other.y)
        else:
            raise Exception("Error in math operation")

    def __isub__(self, other):
        if other.__class__ == Vec2:
            self.x -= other.x
            self.y -= other.y
        else:
            raise Exception("Error in math operation")

    def LenSqr(self):
        return real(self.x ** 2 + self.y ** 2)

    def Len(self):
        return real(math.sqrt(self.x ** 2 + self.y ** 2))

    def Rotate(self, radians: real):
        c = math.cos(radians)
        s = math.sin(radians)
        xp = self.x * c - self.y * s
        yp = self.x * s + self.y * c
        self.x = real(xp)
        self.y = real(yp)

    def Normalize(self):
        _len = self.Len()
        if _len > EPSILON:
            inv_len = 1.0 / _len
            self.x *= inv_len
            self.y *= inv_len


class Mat2:
    def __init__(self, a1: real = None, a2: real = None, a3: real = None, a4: real = None):
        self.m00 = real(0)
        self.m01 = real(0)
        self.m10 = real(0)
        self.m11 = real(0)
        self.m = [[real(0), real(0)], [real(0), real(0)]]
        self.v = [real(0), real(0), real(0), real(0)]
        if not None in [a1, a2, a3, a4]:
            self.m00 = a1
            self.m01 = a2
            self.m10 = a3
            self.m11 = a4
        elif not a1 is None:
            c = math.cos(a1)
            s = math.sin(a1)
            self.m00 = real(c)
            self.m01 = real(-s)
            self.m10 = real(s)
            self.m11 = real(c)

    def Set(self, radians: real):
        c = math.cos(radians)
        s = math.sin(radians)
        self.m00 = real(c)
        self.m01 = real(-s)
        self.m10 = real(s)
        self.m11 = real(c)

    def Abs(self):
        return Mat2(real(abs(self.m00)), real(abs(self.m01)),
                    real(abs(self.m10)), real(abs(self.m11)))

    def AxisX(self):
        return Vec2(self.m00, self.m10)

    def AxisY(self):
        return Vec2(self.m01, self.m11)

    def Transpose(self):
        return Mat2(self.m00, self.m01, self.m10, self.m11)

    def __mul__(self, other):
        if other.__class__ == Vec2:
            return Vec2(self.m00 * other.x + self.m01 * other.y,
                        self.m10 * other.x + self.m11 * other.y)
        elif other.__class__ == Mat2:
            return Mat2(
                self.m[0][0] * other.m[0][0] + self.m[0][1] * other.m[1][0],
                self.m[0][0] * other.m[0][1] + self.m[0][1] * other.m[1][1],
                self.m[1][0] * other.m[0][0] + self.m[1][1] * other.m[1][0],
                self.m[1][0] * other.m[0][1] + self.m[1][1] * other.m[1][1]
            )
        else:
            raise Exception("Error in math operation")


def Min(a: Vec2, b: Vec2):
    return Vec2(min(a.x, b.x), min(a.y, b.y))


def Max(a: Vec2, b: Vec2):
    return Vec2(max(a.x, b.x), max(a.y, b.y))


def Dot(a: Vec2, b: Vec2):
    return real(a.x * b.x + a.y * b.y)


def DistSqr(a: Vec2, b: Vec2):
    c = a - b
    return Dot(c, c)


def Cross(a: Vec2 or real, b: real or Vec2):
    if a.__class__ == Vec2 and b.__class__ == real:
        return Vec2(b * a.y, -b * a.x)
    elif a.__class__ == real and b.__class__ == Vec2:
        return Vec2(a * b.y, -a * b.x)
    elif a.__class__ == Vec2 and b.__class__ == Vec2:
        return real(a.x * b.y - a.y * b.x)
    else:
        raise Exception("Error in Cross")


def Equal(a: real, b: real):
    return abs(a - b) <= EPSILON


def Sqr(a: real):
    return real(a * a)


def Clamp(min: real, max: real, a: real):
    if a < min:
        return min
    elif a > max:
        return max
    else:
        return a


def Round(a: real):
    return int32(a + 0.5)


def Random(l: real, h: real):
    return real(random.uniform(l, h))


def BiasGreaterThan(a: real, b: real):
    k_biasRelative = 0.95
    k_biasAbsolute = 0.01
    return a >= b * k_biasRelative + a * k_biasAbsolute


gravityScale = 5.0
gravity = Vec2(real(0), real(10 * gravityScale))
dt = 1.0 / 60.0