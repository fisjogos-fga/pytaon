from typing import Union, Tuple
from numbers import Number
from math import sqrt, pi
from functools import singledispatch

from .vec2d import Vec2d, VecLike, asvec2d
from .mat2 import Mat2, asmat2

RADS_TO_DEGREES = 180 / pi
DEGREES_TO_RADS = pi / 180


class Transform:
    """
    Transformação afim em 2D.

    Multiplicação de transformações afins é entendida como encadeamento de transformações.
    Uma transformação afim multiplicada por um vetor realiza a transformação neste vetor.

    A transformação é criada a partir dos atributos:
        
        [[a, c, tx],
         [b, d, ty]]
    """

    # Propriedades e atributos
    a: float
    b: float
    c: float
    d: float
    tx: float
    ty: float

    @property
    def matrix(self):
        """
        Matriz implícita na transformação afim.
        """
        return Mat2(self.a, self.b, self.c, self.d)

    @matrix.setter
    def matrix(self, value):
        self.a, self.b, self.c, self.d = value.flat()

    @property
    def vector(self):
        """
        Vetor de translação da transformação afim.
        """
        return Vec2d(self.tx, self.ty)

    @vector.setter
    def vector(self, value):
        self.tx, self.ty = value

    # Construtores alternativos
    @classmethod
    def affine(cls, mat=None, translation=(0, 0)):
        """
        Cria transformação afim a partir da matriz de transformação linear e 
        um vetor de deslocamento
        """
        m = Mat2.identity() if mat is None else mat
        x, y = translation
        return cls(m.a, m.b, m.c, m.d, x, y)

    @classmethod
    def identity(cls):
        """
        Cria transformação de identidade.
        """
        return cls.scale(1, 1)

    @classmethod
    def rotation(cls, angle, translation=(0, 0)):
        """
        Cria uma transformação de rotação (ângulo em radianos).
        """
        return cls.affine(Mat2.rotation(angle), translation)

    @classmethod
    def rotation_degrees(cls, angle, translation=(0, 0)):
        """
        Cria uma transformação de rotação (ângulo em graus).
        """
        return cls.rotation(angle * DEGREES_TO_RADS, translation)

    @classmethod
    def projection(cls, angle, translation=(0, 0)):
        """
        Cria uma transformação de projeção (ângulo em radianos).
        """
        return cls.affine(Mat2.projection(angle), translation)

    @classmethod
    def projection_degrees(cls, angle, translation=(0, 0)):
        """
        Cria uma transformação de projeção (ângulo em graus).
        """
        return cls.projection(angle * DEGREES_TO_RADS, translation)

    @classmethod
    def scale(cls, scale_x, scale_y=None, translation=(0, 0)):
        """
        Cria transformação de escala.
        """
        return cls.affine(Mat2.scale(scale_x, scale_y), translation)

    @classmethod
    def similarity(
        cls, *, scale=None, angle=None, angle_degrees=None, translation=(0, 0)
    ):
        """
        Cria transformação de similaridade a partir de operação fundamental.
        """
        if angle is not None:
            M = Mat2.rotation(angle)
        elif angle_degrees is not None:
            M = Mat2.rotation(angle_degrees)
        else:
            M = Mat2.identity()
        vec = Vec2d(*translation)

        if scale is not None:
            vec *= scale
            M = Mat2.scale(scale) * M

        return cls.affine(M, vec)

    def __init__(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
        self.a = a + 0.0
        self.b = b + 0.0
        self.c = c + 0.0
        self.d = d + 0.0
        self.tx = tx + 0.0
        self.ty = ty + 0.0

    def __mul__(self, other):
        if isinstance(other, Mat2):
            return Transform.affine(other * self.matrix, other.T * self.vector)
        elif isinstance(other, Transform):
            M = self.matrix
            return Transform.affine(M * other.matrix, self.vector + M * other.vector)
        elif isinstance(other, (tuple, Vec2d)):
            return self.transform_vector(other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Mat2):
            return Transform.affine(other * self.matrix, other * self.vector)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            M = self.matrix
            return Transform.affine(M, self.vector + M * other)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            return Transform.affine(self.matrix, self.vector + other)
        return NotImplemented

    # Comparações
    def __eq__(self, other):
        if isinstance(other, Transform):
            return (
                self.a == other.a
                and self.b == other.b
                and self.c == other.c
                and self.d == other.d
                and self.tx == other.tx
                and self.ty == other.ty
            )
        return NotImplemented

    # Métodos da classe
    def copy(self):
        """
        Retorna cópia da transformação afim.
        """
        return Transform(self.a, self.b, self.c, self.d, self.tx, self.ty)

    def mutate_vector(self, vec: Vec2d):
        """
        Transforma vetor por transformação  afim.
        """
        vec.x, vec.y = self.transform_vector(vec)

    def transform_vector(self, vec: VecLike):
        """
        Transforma vetor por transformação  afim.
        """
        return self.matrix.transform_vector(vec) + self.vector


#
# Funções auxiliares
#
def astransform(obj) -> "Transform":
    """
    Converte objeto para Transform, caso não seja. 
    """
    if isinstance(obj, Transform):
        return obj
    elif isinstance(obj, Mat2):
        return Transform.affine(obj, (0, 0))
    elif isinstance(obj, (tuple, list, Vec2d)):
        return Transform.affine(Mat2.identity(), asvec2d(obj))
    kind = type(obj).__name__  # Extrai nome do tipo de obj.
    raise TypeError(f"não pode converter {kind} em Transform")


@singledispatch
def transform(obj, transform: Transform):
    """
    Retorna cópia de objeto transformado pela transformação afim dada.
    """
    new = obj.copy()
    transform(new)
    return new


@singledispatch
def mutate_by(obj, transform: Transform):
    """
    Transforma objeto pela transformação afim dada.
    """
    raise NotImplementedError
