from IEMath import *


class Body:
    def __init__(self, shape_, x: int, y: int):
        self.shape = shape_.Clone()
        shape_.body = self

        self.position = Vec2(real(x), real(y))
        self.velocity = Vec2(real(0), real(0))

        self.angularVelocity = real(0)
        self.torque = real(0)
        self.orient = Random(-PI, PI)

        self.force = Vec2(real(0), real(0))

        self.staticFriction = real(0.5)
        self.dynamicFriction = real(0.3)
        self.restitution = real(0.2)

        self.shape.Initialize()

        self.I = real(0)
        self.iI = real(0)
        self.m = real(0)
        self.im = real(0)

        self.r = Random(real(0.2), real(0.1))
        self.g = Random(real(0.2), real(0.1))
        self.b = Random(real(0.2), real(0.1))

    def ApplyForce(self, f: Vec2):
        self.force += f

    def ApplyImpulse(self, impulse: Vec2, contactVector: Vec2):
        self.velocity += self.im * impulse
        self.angularVelocity += self.iI * Cross(contactVector, impulse)

    def SetStatic(self):
        self.I = real(0)
        self.iI = real(0)
        self.m = real(0)
        self.im = real(0)

    def SetOrient(self, radians: real):
        self.orient = radians
        self.shape.SetOrient(radians)
