"""
Funções que retornam funções de força.
"""
from functools import partial

from .body import Body


def gravity(body_a: Body, body_b: Body, G=None, alpha=2):
    """
    Retorna um par de forças gravitacionais entre dois objetos.

    Exemplo:
    >>> planet.force_func, sun.force_func = gravity(planet, sun)
    """

    def force(a: Body, b: Body, time: float):
        dist = a.position - b.position
        n = dist.normalized()
        return -(G * a.mass * b.mass / dist.length ** alpha) * n

    return partial(force, body_b), partial(force, body_a)
