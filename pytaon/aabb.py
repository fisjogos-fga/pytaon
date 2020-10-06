import pyxel

from .body import Body
from .collision import Collision


class AABB(Body):
    """
    Objeto com caixa de contorno retangular e alinhada aos eixos. 
    """

    left = right = top = bottom = None

    @property
    def area(self):
        return self.width * self.height

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.top - self.bottom

    @property
    def position_x(self):
        return (self.left + self.right) / 2

    @position_x.setter
    def position_x(self, value):
        dx = value - self.position_x
        self.left += dx
        self.right += dx

    @property
    def position_y(self):
        return (self.bottom + self.top) / 2

    @position_y.setter
    def position_y(self, value):
        dy = value - self.position_y
        self.bottom += dy
        self.top += dy

    def __init__(self, left, bottom, right, top, *args, **kwargs):
        assert left <= right
        assert bottom <= top
        self.left, self.right, self.bottom, self.top = left, right, bottom, top
        super().__init__((self.position_x, self.position_y), *args, **kwargs)

    def draw(self):
        pyxel.rect(self.left, self.bottom, self.width, self.height, self.color)

    def update_position(self, dt):
        dx = self.velocity_x * dt
        dy = self.velocity_y * dt
        self.left += dx
        self.right += dx
        self.bottom += dy
        self.top += dy

    def get_collision(self, other):
        return other.get_collision_aabb(self)

    def get_collision_aabb(self, other):
        ax = max(self.left, other.left)
        bx = min(self.right, other.right)
        ay = max(self.bottom, other.bottom)
        by = min(self.top, other.top)

        if ax < bx and ay < by:
            pos = ((ax + bx) / 2, (ay + by) / 2)
            if bx - ax < by - ay:
                normal = (1, 0)
            else:
                normal = (0, 1)
            return Collision(self, other, pos, normal)
