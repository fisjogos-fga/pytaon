from math import pi, sqrt

import pyxel

from .body import Body
from .collision import Collision


class Circle(Body):
    """
    Corpo físico com caixa de contorno circular.
    """

    @property
    def area(self):
        return pi * self.radius ** 2

    right = property(lambda self: self.position.x + self.radius)
    left = property(lambda self: self.position.x - self.radius)
    top = property(lambda self: self.position.y + self.radius)
    bottom = property(lambda self: self.position.y - self.radius)

    def __init__(self, radius, *args, **kwargs):
        self.radius = radius
        super().__init__(*args, **kwargs)

    def draw(self):
        pyxel.circ(*self.position, self.radius, self.color)

    def get_collision(self, other):
        return other.get_collision_circle(self)

    def get_collision_circle(self, other):
        dx, dy = self.position - other.position
        distance = sqrt(dx ** 2 + dy ** 2)

        if distance <= self.radius + other.radius:
            return Collision(self, other, (0, 0), (0, 0))
        else:
            return None
