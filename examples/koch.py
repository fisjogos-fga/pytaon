import random
from itertools import chain, islice, cycle
from math import sqrt

import pyxel
from pytaon import Vec2d


def koch(u, v, n):
    if n == 0:
        yield (*u, *v)
        return

    delta = (v - u) / 3
    a, c = u + delta, u + 2 * delta
    b = a + delta.rotated_degrees(-60)

    yield from koch(u, a, n - 1)
    yield from koch(a, b, n - 1)
    yield from koch(b, c, n - 1)
    yield from koch(c, v, n - 1)


def update():
    try:
        cmds.extend(islice(gen, 4))
    except StopIteration:
        pass


def draw():
    pyxel.cls(pyxel.COLOR_BLACK)
    colors = islice(cycle(range(1, 16)), pyxel.frame_count % 15, None)
    for cmd, col in zip(cmds, colors):
        pyxel.line(*cmd, col)


HEIGHTS = range(220, 50, -70)
gen = chain.from_iterable(koch(Vec2d(0, y), Vec2d(256, y), 4) for y in HEIGHTS)
cmds = []
pyxel.init(256, 256, caption="Koch Fractal", fps=30)
pyxel.run(update, draw)
