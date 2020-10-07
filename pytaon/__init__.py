"""
Physics module for the Pyxel engine.
"""
__version__ = "0.0.2b"

import pyxel as _pyxel
from .body import Body
from .circle import Circle
from .aabb import AABB
from .segment import Segment
from .poly import Poly
from .space import Space
from .collision import Collision
from .vec2d import Vec2d, VecLike, asvec2d
from .mat2 import Mat2, MatLike, asmat2
from .transform import Transform, astransform

# Sobrescrita de funções do Pyxel
def init(width, height, *args, fps=30, **kwargs):
    """
    Inicializa pytaon e grava fps e dt = 1/fps como parâmetros
    do módulo.
    """
    _pyxel.init(width, height, *args, fps=fps, **kwargs)

    globals()["fps"] = fps
    globals()["dt"] = 1 / fps


def run(*args, background=_pyxel.COLOR_BLACK):
    """
    Inicia loop principal.

    Aceita um Space como único argumento ou update() e draw()
    como argumentos separados.
    """
    if len(args) == 1:
        (sp,) = args

        def update():
            sp.step(globals()["dt"])

        def draw():
            if background is not None:
                _pyxel.cls(background)
            sp.draw()

        return _pyxel.run(update, draw)
    else:
        return _pyxel.run(*args)


# Constantes
ii = Vec2d(1, 0)
jj = Vec2d(0, 1)


# Atributos calculados
def __getattr__(attr):
    """
    __getattr__ é chamando sempre que o usuário pedir um símbolo
    que não existe no módulo pytaon. Isto permite calcular valores
    em tempo de execução.
    """
    try:
        return globals()[f"_{attr}_"]()
    except KeyError:
        return getattr(_pyxel, attr)


def _middle_():
    return Vec2d(_pyxel.width / 2, _pyxel.height / 2)


def _mouse_pos_():
    return Vec2d(_pyxel.mouse_x / 2, _pyxel.mouse_y / 2)
