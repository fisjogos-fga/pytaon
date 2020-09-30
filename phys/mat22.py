from typing import Union, Tuple
from numbers import Number
from math import sqrt, pi

from .vec2d import Vec2d, VecLike

MatLike = Union["Mat2", Tuple[Tuple[Number, Number], Tuple[Number, Number]]]
RADS_TO_DEGREES = 180 / pi
DEGREES_TO_RADS = pi / 180


class Mat2:
    """
    Matriz 2x2. Suporta operações básicas e mostra propriedades da matriz como métodos.

    Matriz é entendida como uma sequência de vetores linha. 

    Matriz é criada a partir dos atributos:
        
        [[a, c],
         [b, d]]
    """

    # Propriedades e atributos
    a: float
    b: float
    c: float
    d: float

    @property
    def trace(self):
        """
        Traço da matriz.
        """
        raise NotImplementedError

    @property
    def determinant(self):
        """
        Determinante da matriz.
        """
        raise NotImplementedError

    @property
    def T(self):
        return self.transposed()

    # Construtores alternativos
    @classmethod
    def identity(cls):
        """
        Cria uma matriz de escala.
        """
        return cls.scale(1, 1)

    @classmethod
    def rotation(cls, angle):
        """
        Cria uma matriz de rotação (ângulo em radianos).
        """
        raise NotImplementedError

    @classmethod
    def rotation_degrees(cls, angle):
        """
        Cria uma matriz de rotação (ângulo em graus).
        """
        return cls.rotation(angle * DEGREES_TO_RADS)

    @classmethod
    def scale(cls, scale_x, scale_y=None):
        """
        Cria uma matriz de escala.
        """
        raise NotImplementedError

    @classmethod
    def zero(cls):
        """
        Cria matriz nula.
        """
        return cls(0.0, 0.0)

    def __init__(self, *args):
        if len(args) == 2:
            row1, row2 = args
            self.a, self.c = map(float, row1)
            self.b, self.d = map(float, row2)
        else:
            self.a, self.b, self.c, self.d = args

    def __repr__(self):
        return f"Mat2({self.a}, {self.b}, {self.c}, {self.d})"

    # Operações matemáticas
    def __add__(self, other):
        raise NotImplementedError

    def __radd__(self, other):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __isub(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, Mat2):
            raise NotImplementedError
        elif isinstance(other, Number):
            raise NotImplementedError
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Number):
            raise NotImplementedError
        return NotImplemented

    def __imul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __itruediv__(self, other):
        raise NotImplementedError

    # Comparações
    def __eq__(self, other):
        if isinstance(other, Mat2):
            return (
                self.a == other.a
                and self.b == other.b
                and self.c == other.c
                and self.d == other.d
            )
        return NotImplemented

    # Comportamento de sequências
    def __len__(self):
        return 2

    def __iter__(self):
        yield Vec2d(self.a, self.c)
        yield Vec2d(self.b, self.d)

    def __getitem__(self, idx):
        if idx == 0:
            return Vec2d(self.a, self.c)
        elif idx == 1:
            return Vec2d(self.b, self.d)
        elif idx == (0, 0):
            return self.a
        elif idx == (0, 1):
            return self.c
        elif idx == (1, 0):
            return self.b
        elif idx == (1, 1):
            return self.d
        raise IndexError(idx)

    def __setitem__(self, idx, value):
        raise NotImplementedError

    # Métodos da classe
    def copy(self):
        """
        Retorna cópia da matriz.
        """
        raise NotImplementedError

    def interpolate_to(self, other: MatLike, range: float) -> "Mat2":
        """
        Interpola matriz linearmente até other no intervalo controlado por range.

        Range varia de forma que se range=0.0, retorna self, range=1.0 retorna other
        e valores intermediários produzem interpolações. 
        """
        raise NotImplementedError

    def rotate(self, angle: float):
        """
        Rotaciona matriz pelo ângulo em radianos.
        """
        raise NotImplementedError

    def rotate_degrees(self, angle: float):
        """
        Rotaciona matriz pelo ângulo em graus.
        """
        self.rotate(angle * DEGREES_TO_RADS)

    def rotated(self, angle: float) -> "Mat2":
        """
        Cria nova matriz rotacionado ângulo em radianos.
        """
        new = self.copy()
        new.rotate(angle)
        return new

    def rotated_degrees(self, angle: float) -> "Mat2":
        """
        Cria nova matriz rotacionado ângulo em graus.
        """
        return self.rotated(angle * DEGREES_TO_RADS)

    def transform_vector(self, vec: Vec2d):
        """
        Transforma vetor pela matriz.
        """
        vec.x, vec.y = self.transformed_vector(vec)

    def transformed_vector(self, vec: VecLike) -> Vec2d:
        """
        Retorna cópia de vetor transformado pela matriz.

        Mesmo que Mat2 * Vec2d
        """
        x, y = vec
        return Vec2d(x * self.a + y * self.c, x * self.b + y * self.d)

    def transpose(self):
        """
        Transpõe matriz.
        """
        raise NotADirectoryError

    def transposed(self) -> "Mat2":
        """
        Retorna cópia de matriz transposta.
        """
        new = self.copy()
        new.transpose()
        return new


#
# Funções auxiliares
#
def asmat2(obj) -> "Vec2d":
    """
    Converte objeto para Vec2d, caso não seja vetor. 
    """
    if isinstance(obj, Mat2):
        return obj
    elif isinstance(obj, (tuple, list)):
        row1, row2 = obj
        return Mat2(row1, row2)

    kind = type(obj).__name__  # Extrai nome do tipo de obj.
    raise TypeError(f"não pode converter {kind} em Mat2")
