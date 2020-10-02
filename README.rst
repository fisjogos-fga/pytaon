==============
Physics Engine
==============

Motor de jogos simples que utiliza física baseado em Pyxel.

Instalação
==========

Clone este repositório e utilize ``flit install -s`` para instalar localmente.


Tutorial
========

Toda simulação 

.. code-block:: python

    import phys
    
    WIDTH = 120
    HEIGHT = 80
    
We can create geometric figures by calling the corresponding functions in the ``phys`` module. Just like Pyxel, those functions take a color and some geometric quantities as arguments, but they can also support many physical parameters such as mass, moment of inertial, velocities, etc. We must also remember that physical objects are created into a special "stage" instance and only interact with other objects within the same stage. You can create the stage explicitly, but if you don't, the engine creates a default instance for you.

We can create a paddle as a irrotational rectangle:

.. code-block:: python

    p1 = phys.rect(100, 212)
    p2 = phys.rect(100, 212)

Since ``p1`` and ``p2`` have no mass or moment of inertia, the engine assigns an infinite value to those two quantities. An infinite mass is interpreted as an object that do not respond to forces (since it would require an infinite force to make an effect), but may move and even collide with regular dynamic objects. If a velocity is defined (even if equal to zero) we call those objects "kinematic", which in physics means that we can describe their movement but do not want to talk about the forces that cause it. "Dynamic" objects have their movement influenced by forces (including gravity and collisions) and "static" objects are a special kind of kinematic objects that do not move at all. Pymunk, and physics textbooks for that matter, make a distinction between those three situations, so it is good to keep this nomenclature in mind.  
