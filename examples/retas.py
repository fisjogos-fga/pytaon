"""
Equação da reta
===============

Este programa mostra como representar retas utilizando uma parametrização da forma

    R(t) = R0 + n * t,

onde R(t), R0 e n são vetores e t é um parâmetro análogo ao tempo. 
"""

import pyxel
from pytaon import Vec2d


def read_vec(msg) -> Vec2d:
    """
    Pede uma entrada vetorial.
    """
    x, _, y = input(msg).lstrip("[( ").rstrip(")] ").partition(",")
    return Vec2d(float(x), float(y))


def update():
    pyxel.time += pyxel.dt


def draw():
    # Mostra ponto inicial e legenda.
    if pyxel.frame_count == 0:
        pyxel.text(10, 160, "t positivo", pyxel.COLOR_GREEN)
        pyxel.text(10, 170, "t negativo", pyxel.COLOR_RED)
        x, y = pyxel.R0
        pyxel.text(x, pyxel.height - y, str(list(pyxel.R0)), pyxel.COLOR_WHITE)

    # Marca pontos na tela a partir da parametrização da reta.
    dt = pyxel.dt / pyxel.steps
    R0, n = pyxel.R0, pyxel.n

    for i in range(pyxel.steps):
        t = pyxel.time + dt * i

        x1, y1 = R0 + n * t
        x2, y2 = R0 - n * t

        pyxel.pset(x1, pyxel.height - y1, pyxel.COLOR_GREEN)
        pyxel.pset(x2, pyxel.height - y2, pyxel.COLOR_RED)

    # Desenha tempo decorrido no canto inferior direito
    pyxel.time += pyxel.dt
    x, y = (pyxel.width - pyxel.FONT_WIDTH * 14, pyxel.height - pyxel.FONT_HEIGHT)
    pyxel.rect(x, y, pyxel.FONT_WIDTH * 14, pyxel.FONT_HEIGHT, pyxel.COLOR_BLACK)
    pyxel.text(x, y, ("t = %.1f" % pyxel.time).rjust(10), pyxel.COLOR_WHITE)


def main():
    # Pede vetores de entrada para o usuário
    print(__doc__)
    pyxel.R0 = read_vec("R0 [x, y]: ")
    pyxel.n = read_vec("n [x, y]: ")

    # Inicializa o módulo
    pyxel.time = 0.0
    pyxel.steps = 100
    pyxel.dt = 1 / 30
    pyxel.init(240, 180, caption="Retas", fps=30)

    # Roda!
    pyxel.run(update, draw)


if __name__ == "__main__":
    main()
