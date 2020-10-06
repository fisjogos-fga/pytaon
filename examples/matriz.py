"""
Transformações lineares
=======================

Este programa demonstra o efeito de transformações lineares em um grupo de pontos.
"""

import re
import pyxel
from pytaon import Transform, Vec2d


def square():
    """
    Produz pontos que formam um quadrado.
    """
    N = 30
    for i in range(N + 1):
        for j in range(N + 1):
            x = 2.0 * (i / N) - 1.0
            y = 2.0 * (j / N) - 1.0
            yield x, y


def circle():
    """
    Produz pontos que formam um círculo.
    """
    for x, y in square():
        if x ** 2 + y ** 2 <= 1.0:
            yield x, y


def triangle():
    """
    Produz pontos que formam um triângulo.
    """
    for x, y in square():
        if x <= y:
            yield x, y


def update():
    """ 
    Verifica entradas do usuário
    """

    # Reinicia lista de pontos para figura geométrica
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.points = list(square())
    if pyxel.btnp(pyxel.KEY_C):
        pyxel.points = list(circle())
    if pyxel.btnp(pyxel.KEY_T):
        pyxel.points = list(triangle())

    # Desloca figura geométrica no plano
    dl = 0.01
    if pyxel.btn(pyxel.KEY_UP):
        for i, (x, y) in enumerate(pyxel.points):
            pyxel.points[i] = (x, y + dl)
    if pyxel.btn(pyxel.KEY_DOWN):
        for i, (x, y) in enumerate(pyxel.points):
            pyxel.points[i] = (x, y - dl)
    if pyxel.btn(pyxel.KEY_LEFT):
        for i, (x, y) in enumerate(pyxel.points):
            pyxel.points[i] = (x - dl, y)
    if pyxel.btn(pyxel.KEY_RIGHT):
        for i, (x, y) in enumerate(pyxel.points):
            pyxel.points[i] = (x + dl, y)

    # Modifica o tipo de transformação
    if pyxel.btnp(pyxel.KEY_R):
        pyxel.factory = Transform.rotation_degrees
    elif pyxel.btnp(pyxel.KEY_P):
        pyxel.factory = Transform.projection_degrees

    # Altera o ângulo da matriz
    if pyxel.btnp(pyxel.KEY_Z, period=2):
        pyxel.angle += 1
    if pyxel.btnp(pyxel.KEY_X, period=2):
        pyxel.angle -= 1

    # Altera o vetor de translação
    delta = 0.02
    if pyxel.btn(pyxel.KEY_A):
        pyxel.translation.x -= delta
    if pyxel.btn(pyxel.KEY_D):
        pyxel.translation.x += delta
    if pyxel.btn(pyxel.KEY_W):
        pyxel.translation.y += delta
    if pyxel.btn(pyxel.KEY_S):
        pyxel.translation.y -= delta

    pyxel.M = pyxel.factory(pyxel.angle, translation=pyxel.translation)

    # Aplica transformação linear nos pontos (ou não)
    if pyxel.btn(pyxel.KEY_SPACE):
        pyxel.transform = pyxel.M.transform_vector
    else:
        pyxel.transform = None


def draw_points(pts, color):
    """
    Desenha lista de pontos com a cor fornecida.
    """
    scale = 50
    for x, y in pts:
        i = scale * x + 120
        j = pyxel.height - scale * y - 80
        pyxel.pset(i, j, color)


def draw_axis():
    """
    Desenha eixos do sistema de coordenadas.
    """
    pyxel.line(5, 100, 235, 100, pyxel.COLOR_WHITE)
    pyxel.line(235, 100, 232, 98, pyxel.COLOR_WHITE)
    pyxel.line(235, 100, 232, 102, pyxel.COLOR_WHITE)
    pyxel.text(230, 105, "x", pyxel.COLOR_WHITE)

    pyxel.line(120, 25, 120, 175, pyxel.COLOR_WHITE)
    pyxel.line(120, 25, 122, 28, pyxel.COLOR_WHITE)
    pyxel.line(120, 25, 118, 28, pyxel.COLOR_WHITE)
    pyxel.text(125, 22, "y", pyxel.COLOR_WHITE)


def draw_instructions():
    """
    Desenha textos com instruções na tela.
    """
    pyxel.text(5, 0, "Aperte espaco para realizar transformacao", pyxel.COLOR_WHITE)
    pyxel.text(5, 10, "Figuras: [q]uadrado, [c]irculo, [t]riangulo", pyxel.COLOR_RED)
    pyxel.text(5, 20, "Matriz: [r]otacao, [p]rojecao", pyxel.COLOR_PURPLE)

    text = f"angle = {pyxel.angle}"
    pyxel.text(240 - 21 * pyxel.FONT_WIDTH, 155, text, pyxel.COLOR_RED)

    # (a, c), (b, d) = pyxel.M
    # text = "M = %.2f %.2f\n    %.2f %.2f   " % (a, b, c, d)
    # pyxel.text(240 - 21 * pyxel.FONT_WIDTH, 165, text.rjust(20), pyxel.COLOR_LIME)


def draw():
    """
    Desenha conjunto de pontos.
    """
    pyxel.cls(pyxel.COLOR_BLACK)
    draw_points(pyxel.points, pyxel.COLOR_NAVY)
    if pyxel.transform:
        draw_points(map(pyxel.transform, pyxel.points), pyxel.COLOR_LIGHTBLUE)
    draw_instructions()
    draw_axis()


def main():

    # Pede vetores de entrada para o usuário
    print(__doc__)

    pyxel.factory = Transform.rotation_degrees
    pyxel.translation = Vec2d(0, 0)
    pyxel.angle = 0
    pyxel.M = pyxel.factory(pyxel.angle)
    pyxel.points = list(square())
    pyxel.transform = None

    # Inicializa o módulo e roda!
    pyxel.init(240, 180, caption="Retas", fps=30)
    pyxel.mouse(True)
    pyxel.run(update, draw)


if __name__ == "__main__":
    main()
