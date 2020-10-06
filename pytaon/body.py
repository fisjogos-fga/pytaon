import pyxel
import random
from math import sqrt

from .collision import Collision
from .vec2d import Vec2d, asvec2d


class Body:
    """
    Representa uma partícula ou corpo rígido com velocidade e posição bem 
    definidas.

    Cada sub-classe de Body representa um tipo diferente de caixa de contorno.
    """

    # Propriedades genéricas
    position: Vec2d = None
    velocity: Vec2d = None
    force: Vec2d = None
    position_x = property(
        lambda self: self.position.x,
        lambda self, value: setattr(self.position, "x", value),
    )
    position_y = property(
        lambda self: self.position.y,
        lambda self, value: setattr(self.position, "y", value),
    )
    velocity_x = property(
        lambda self: self.velocity.x,
        lambda self, value: setattr(self.velocity, "x", value),
    )
    velocity_y = property(
        lambda self: self.velocity.y,
        lambda self, value: setattr(self.velocity, "y", value),
    )

    @property
    def area(self):
        """
        Área da figura geométrica.
        """
        name = type(self).__name__
        raise NotImplementedError(f"Corpo {name} não implementa área")

    @property
    def density(self):
        """
        Densidade do objeto.
        """
        return self.mass / self.area if self.area else float("inf")

    @density.setter
    def density(self, value):
        self.mass *= value / self.density

    @property
    def kinetic_energy(self):
        """
        Energia cinética associada ao corpo.
        """
        raise NotImplementedError

    @property
    def right(self):
        """
        Coordenada x da margem direita do corpo.
        """
        raise NotImplementedError

    @property
    def left(self):
        """
        Coordenada x da margem esquerda do corpo.
        """
        raise NotImplementedError

    @property
    def top(self):
        """
        Coordenada y da margem superior do corpo.
        """
        raise NotImplementedError

    @property
    def bottom(self):
        """
        Coordenada y da margem inferior do corpo.
        """
        raise NotImplementedError

    def __init__(
        self,
        pos=(0, 0),
        vel=(0, 0),
        mass=1.0,
        color=0,
        damping=None,
        gravity=None,
        restitution=None,
    ):
        self.position = Vec2d(*pos)
        self.velocity = Vec2d(*vel)
        self.mass = float(mass)
        self.color = color
        self.force = Vec2d(0, 0)
        self.damping = None if damping is None else float(damping)
        self.gravity = None if gravity is None else asvec2d(gravity)
        self.restitution = None if restitution is None else float(restitution)

    def apply_force(self, fx, fy=None):
        """
        Aplica força ao objeto.

        Este método é cumulativo e permite que várias forças sejam acumuladas
        ao mesmo objeto em cada passo de simulação.
        """
        if fy is not None:
            fx = Vec2d(fx, fy)
        self.force += fx

    def update_velocity(self, dt):
        """
        Atualiza velocidades de acordo com as forças acumuladas até o presente
        frame.
        """
        acc = self.force / self.mass
        self.velocity += acc * dt
        self.force *= 0.0

    def update_position(self, dt):
        """
        Atualiza posições de acordo com as velocidades.
        """
        self.position += self.velocity * dt

    def draw(self):
        """
        Desenha figura na tela.
        """
        pyxel.pset(*self.position, self.color)

    #
    # Calcula colisões com outras figuras geométricas.
    #
    def get_collision(self, other: "Body") -> "Collision":
        """
        Verifica se há colisão com outro objeto e retorna um objeto de colisão 
        ou None caso não exista superposição.
        """
        msg = f"Colisão não implementada: {type(self)}, {type(other)}"
        raise NotImplementedError(msg)

    def get_collision_circle(self, other: "Circle"):
        """
        Verifica colisão com círculos.
        """
        raise NotImplementedError("Implemente em sub-classe")

    def get_collision_aabb(self, other):
        """
        Verifica colisão com AABBs.
        """
        raise NotImplementedError("Implemente em sub-classe")

    def get_collision_poly(self, other):
        """
        Verifica colisão com Polígonos.
        """
        raise NotImplementedError("Implemente em sub-classe")

    def get_collision_segment(self, other):
        """
        Verifica colisão com Pílulas.
        """
        raise NotImplementedError("Implemente em sub-classe")
