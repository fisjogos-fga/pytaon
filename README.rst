======
PyTaOn
======

Motor de jogos simples que utiliza física baseado em Pyxel.

Instalação
==========

Clone este repositório e utilize ``flit install -s`` para instalar localmente.
Em breve teremos suporte para ``pip install pytaon`` ;-).


Tutorial
========

Criamos uma simulação simples de duas caixas sujeitas à lei da gravidade.

.. code-block:: python

    import pytaon as on
    import pyxel
    
    WIDTH = 120
    HEIGHT = 80
    
Criamos os objetos de jogo, junto ao espaço correspondente

.. code-block:: python

    sp = on.Space()
    bola = sp.add_circle(5, (120, 90), color=pyxel.COLOR_RED)
    chao = sp.add_aabb(0, 160, 240, 180, color=pyxel.COLOR_LIME, mass="inf")
    bola.gravity = (0, 20)

Iniciamos a simulação passando as funções update e draw para o pyxel.


.. code-block:: python
    
    def update():
        sp.update(1/30)
    
    def draw():
        pyxel.cls(pyxel.COLOR_BLACK)
        sp.draw()

    pyxel.init(240, 180, fps=30)
    pyxel.run(update, draw)
