from typing import List

import pyxel

from .body import Body
from .circle import Circle
from .aabb import AABB
from .poly import Poly
from .segment import Segment
from .vec2d import Vec2d, VecLike, asvec2d

MARGIN_WIDTH = 200


class Space:
    """
    Representa um grupo de objetos que interagem entre si.
    """

    bodies: List[Body]

    def __init__(
        self,
        damping=0.0,
        gravity=(0, 0),
        restitution=1.0,
        margin_left=None,
        margin_right=None,
        margin_top=None,
        margin_bottom=None,
    ):
        self.time = 0.0
        self.current_time_step = 0.0
        self.bodies = []
        self.damping = float(damping)
        self.gravity = asvec2d(gravity)
        self.restitution = float(restitution)
        self.margin_right = margin_right
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

    def __contains__(self, body):
        return body in self.bodies

    #
    # Criação e remoção de objetos
    #
    def add(self, body):
        """
        Adiciona objeto ao espaço.
        """
        self.bodies.append(body)

    def _add_object(self, cls, *args, **kwargs) -> Body:
        obj = cls(*args, **kwargs)
        self.add(obj)
        return obj

    def add_circle(self, *args, **kwargs) -> Circle:
        """
        Cria círculo e adiciona ao espaço.
        """
        return self._add_object(Circle, *args, **kwargs)

    def add_aabb(self, *args, **kwargs) -> "Circle":
        """
        Cria AABB e adiciona ao espaço.
        """
        return self._add_object(AABB, *args, **kwargs)

    def add_poly(self, *args, **kwargs) -> "Circle":
        """
        Cria polígono e adiciona ao espaço.
        """
        return self._add_object(Poly, *args, **kwargs)

    def add_segment(self, *args, **kwargs) -> "Circle":
        """
        Cria segmento e adiciona ao espaço.
        """
        return self._add_object(Segment, *args, **kwargs)

    def remove(self, obj):
        """
        Remove objeto da simulação.
        """
        raise NotImplementedError

    # Verifica colisões e pontos
    def point_query(self, vec: VecLike) -> List[Body]:
        """
        Retorna a lista de todos objetos que tocam o ponto dado.
        """
        raise NotImplementedError

    #
    # Simulação
    #
    def step(self, dt):
        """
        Executa um passo de simulação.
        """
        self.current_time_step = dt

        # Aplica forças globais de gravidade e damping. Estas forças são independentes
        # da massa e atuam diretamente na aceleração.
        damping = self.damping
        gravity = self.gravity
        for body in self.bodies:
            damping = damping if body.damping is None else body.damping
            gravity = gravity if body.gravity is None else body.gravity
            body.velocity += (gravity - damping * body.velocity) * dt

        # Atualiza as velocidades dos corpos em função das forças acumuladas.
        for body in self.bodies:
            body.update_velocity(dt)

        # Resolve as colisões.
        for collision in self.get_collisions():
            collision.resolve()

        # Finalmente atualiza as posições.
        for body in self.bodies:
            body.update_position(dt)

        self.time += dt

    def get_collisions(self):
        """
        Retorna sequência de colisões para o frame.
        """
        for i, obj_a in enumerate(self.bodies):
            for obj_b in self.bodies[i + 1 :]:
                col = obj_a.get_collision(obj_b)
                if col is not None:
                    yield col

        self._apply_collision_with_margins()

    def _apply_collision_with_margins(self):
        # Margem esquerda
        if self.margin_left is not None:
            margin = self.margin_left
            for body in self.bodies:
                if body.left <= margin:
                    e = body.restitution
                    body.velocity.y *= -1 if e is None else -e

        # Margem direita
        NotImplemented

        # Margem superior
        NotImplemented

        # Margem inferior
        NotImplemented

    #
    # Outras funções
    #
    def draw(self, *, background=None):
        """
        Desenha o espaço chamando a função .draw() de cada elemento do espaço.
        """

        if background is not None:
            pyxel.cls(background)

        for body in self.bodies:
            body.draw()

    def add_default_collision_handler(self, pre_solve=None, post_solve=None):
        """
        Registra o CollisionHandler padrão para colisões que não possuem um 
        método mais específico associado. 
        """
        raise NotImplementedError

    def add_wildcard_collision_handler(self, col_type, pre_solve=None, post_solve=None):
        """
        Registra o CollisionHandler padrão para colisões que não possuem um 
        método mais específico associado. 
        """
        raise NotImplementedError

    def add_collision_handler(
        self, col_type_a, col_type_b, pre_solve=None, post_solve=None
    ):
        """
        Retorna um CollisionHandler para colisões entre col_type_a e 
        col_type_b. Os tipos equivalem às classes dos objetos e não 
        consideram sub-classes.
        """
        raise NotImplementedError


class CollisionHandler:
    """
    Objeto responsável por processar colisões. 
    
    Possui dois atributos correspondendo a funções:

    * pre_solve: Executada antes de processar a colisão e deve retornar um valor 
      verdadeiro para prosseguir com o processamento da colisão ou falso para desativá-la.
    * post_solve: Executada após resolver as forças e atualizar as velocidades e
      posições dos objetos.
    """

    def __init__(self, pre_solve=None, post_solve=None):
        self.pre_solve = pre_solve or (lambda col: True)
        self.post_solve = post_solve or (lambda col: None)
