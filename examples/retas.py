"""
Equação da reta
===============

Este programa mostra como representar retas utilizando uma parametrização da forma

    R(t) = R0 + n * t,

onde R(t), R0 e n são vetores e t é um parâmetro análogo ao tempo. 
"""

import pytaon as on
from pytaon import Vec2d


def read_vec(msg) -> Vec2d:
    """
    Pede uma entrada vetorial.
    """
    x, _, y = input(msg).lstrip("[( ").rstrip(")] ").partition(",")
    return Vec2d(float(x), float(y))


def update():
    on.time += on.dt


def draw():
    # Mostra ponto inicial e legenda.
    if on.frame_count == 0:
        x, y = on.middle
        on.line(0, y, on.width, y, on.COLOR_PURPLE)
        on.line(x, 0, x, on.height, on.COLOR_PURPLE)

        on.text(10, 160, "t positivo", on.COLOR_GREEN)
        on.text(10, 170, "t negativo", on.COLOR_RED)
        x, y = on.R0 + on.middle
        on.text(x, on.height - y, str(list(on.R0)), on.COLOR_WHITE)

    # Marca pontos na tela a partir da parametrização da reta.
    dt = on.dt / on.steps
    R0, n = on.R0, on.n
    R0 = R0 + on.middle

    for i in range(on.steps):
        t = on.time + dt * i

        x1, y1 = R0 + n * t
        x2, y2 = R0 - n * t

        on.pset(x1, on.height - y1, on.COLOR_GREEN)
        on.pset(x2, on.height - y2, on.COLOR_RED)

    # Desenha tempo decorrido no canto inferior direito
    on.time += on.dt
    x, y = (on.width - on.FONT_WIDTH * 14, on.height - on.FONT_HEIGHT)
    on.rect(x, y, on.FONT_WIDTH * 14, on.FONT_HEIGHT, on.COLOR_BLACK)
    on.text(x, y, ("t = %.1f" % on.time).rjust(10), on.COLOR_WHITE)


def main():
    # Pede vetores de entrada para o usuário
    print(__doc__)
    on.R0 = read_vec("R0 [x, y]: ")
    on.n = read_vec("n [x, y]: ")

    # Inicializa o módulo
    on.time = 0.0
    on.steps = 100
    on.dt = 1 / 30
    on.init(240, 180, caption="Retas", fps=30)

    # Roda!
    on.run(update, draw)


if __name__ == "__main__":
    main()
