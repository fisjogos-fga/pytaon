from typing import Union, Tuple
from numbers import Number
from math import sqrt, cos, sin, pi

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
        return self.a + self.d

    @property
    def determinant(self):
        """
        Determinante da matriz.
        """
        return self.a * self.d - self.b * self.c

    @property
    def T(self):
        """
        Atributo que contêm a matriz transposta.
        """
        return self.transposed()

    @property
    def rows(self):
        """
        Dupla de vetores linha.
        """
        return (Vec2d(self.a, self.c), Vec2d(self.b, self.d))

    @property
    def cols(self):
        """
        Dupla de vetores coluna.
        """
        return (Vec2d(self.a, self.b), Vec2d(self.c, self.d))

    @property
    def eigenvalues(self):
        """
        Lista os dois autovalores da matriz.
        """
        a, b, c, d = self.flat()
        aux = d ** 2 - 2 * a * d + a ** 2 + 4 * c * b
        aux = sqrt(aux) if aux >= 0 else sqrt(-aux) * 1j
        return ((d + a + aux) / 2, (d + a - aux) / 2)

    @property
    def eigenvectors(self):
        """
        Lista dos dois autovetores associados a cada autovalor.
        """
        l1, l2 = self.eigenvalues
        v1 = Vec2d(self.c / (l1 - self.a), 1)
        v2 = Vec2d(self.c / (l2 - self.a), 1)
        return v1.normalized(), v2.normalized()

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
        cos_ = cos(angle)
        sin_ = sin(angle)
        return cls(cos_, sin_, -sin_, cos_)

    @classmethod
    def projection(cls, angle):
        """
        Cria uma matriz de projeção (ângulo em radianos).
        """
        cos_ = cos(angle)
        sin_ = sin(angle)
        diag = cos_ * sin_
        return cls(cos_ ** 2, diag, diag, sin_ ** 2)

    @classmethod
    def projection_degrees(cls, angle):
        """
        Cria uma matriz de projeção (ângulo em graus).
        """
        return cls.projection(angle * DEGREES_TO_RADS)

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
        if scale_y is None:
            scale_y = scale_x
        return cls(scale_x, 0, 0, scale_y)

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
        if isinstance(other, Mat2):
            return Mat2(
                self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d
            )
        return NotImplemented

    def __radd__(self, other):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, Mat2):
            return Mat2(
                self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d
            )
        return NotImplemented

    def __rsub__(self, other):
        raise NotImplementedError

    def __isub(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, Mat2):
            raise NotImplementedError
        elif isinstance(other, Number):
            raise NotImplementedError
        elif isinstance(other, Vec2d):
            return self.transform_vector(other)
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

    def flat(self):
        """
        Retorna sequência com componentes a, b, c e d.
        """
        yield self.a
        yield self.b
        yield self.c
        yield self.d

    def interpolate_to(self, other: MatLike, range: float) -> "Mat2":
        """
        Interpola matriz linearmente até other no intervalo controlado por range.

        Range varia de forma que se range=0.0, retorna self, range=1.0 retorna other
        e valores intermediários produzem interpolações. 
        """
        raise NotImplementedError

    def inverse(self):
        """
        Retorna matrix inversa tal qual M.inverse() * M = Mat2.identity()
        """
        det = self.determinant
        return Mat2(self.d / det, -self.b / det, -self.c / det, self.a / det)

    def rotate(self, angle: float):
        """
        Rotaciona matriz pelo ângulo em radianos.
        """
        self.a, self.b, self.c, self.d = self.rotated(angle)

    def rotate_degrees(self, angle: float):
        """
        Rotaciona matriz pelo ângulo em graus.
        """
        self.rotate(angle * DEGREES_TO_RADS)

    def rotated(self, angle: float) -> "Mat2":
        """
        Cria nova matriz rotacionado ângulo em radianos.
        """
        raise NotImplementedError

    def rotated_degrees(self, angle: float) -> "Mat2":
        """
        Cria nova matriz rotacionado ângulo em graus.
        """
        return self.rotated(angle * DEGREES_TO_RADS)

    def mutate_vector(self, vec: Vec2d):
        """
        Transforma vetor pela matriz, modificando o argumento.
        """
        vec.x, vec.y = self.transform_vector(vec)

    def transform_vector(self, vec: VecLike) -> Vec2d:
        """
        Retorna cópia de vetor transformado pela matriz.

        Mesmo que Mat2 * Vec2d
        """
        x, y = vec
        return Vec2d(self.a * x + self.c * y, self.b * x + self.d * y)

    def transpose(self):
        """
        Transpõe matriz.
        """
        self.b, self.c = self.c, self.b

    def transposed(self) -> "Mat2":
        """
        Retorna cópia de matriz transposta.
        """
        return Mat2(self.a, self.c, self.b, self.d)


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
