from typing import Union, Tuple
from numbers import Number
from math import sqrt, pi, cos, sin, acos, asin, atan2, degrees

VecLike = Union["Vec2d", Tuple[Number, Number]]
RADS_TO_DEGREES = 180 / pi
DEGREES_TO_RADS = pi / 180


class Vec2d:
    """
    Vetor em 2 dimensões. Suporta operações básicas e mostra propriedades do
    vetor como métodos.
    """

    # Propriedades e atributos
    x: float
    y: float

    @property
    def angle(self):
        """
        Ângulo com relação ao eixo x em radianos.
        """
        return atan2(self.y, self.x)

    @angle.setter
    def angle(self, value):
        raise NotImplementedError

    @property
    def angle_degrees(self):
        """
        Ângulo com relação ao eixo x em graus.
        """
        return RADS_TO_DEGREES * self.angle

    @angle_degrees.setter
    def angle_degrees(self, value):
        raise NotImplementedError

    @property
    def length(self):
        """
        Módulo do vetor.
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    @length.setter
    def length(self, value):
        raise NotImplementedError

    @property
    def length_sqrd(self):
        """
        Módulo do vetor ao quadrado.
        """
        return self.length**2

    @property
    def unit(self) -> "Vec2d":
        """
        Vetor unitário na direção do vetor.
        """
        return self / self.length

    # Métodos estáticos
    @classmethod
    def unit_x(cls) -> "Vec2d":
        """
        Vetor unitário na direção x.
        """
        return cls(1.0, 0.0)

    @classmethod
    def unit_y(cls) -> "Vec2d":
        """
        Vetor unitário na direção y.
        """
        return cls(0.0, 1.0)

    @classmethod
    def zero(cls):
        """
        Vetor de tamanho nulo.
        """
        return cls(0.0, 0.0)

    def __init__(self, x, y=None):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Vec2d({self.x}, {self.y})"

    def __neg__(self):
        raise NotImplementedError

    def __pos__(self):
        raise NotImplementedError

    def __abs__(self):
        return self.length

    # Operações matemáticas
    def __add__(self, other):  # self + other
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return Vec2d(self.x + x, self.y + y)
        return NotImplemented

    __radd__ = __add__  # other + self == self + other

    def __iadd__(self, other):  # self += other
        x, y = other
        self.x += x
        self.y += y
        return self

    def __sub__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return Vec2d(self.x - x, self.y - y)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            x,y = other
            return Vec2d(x - self.x, y - self.y)

    def __isub__(self, other):
        x, y = other
        self.x -= x
        self.y -= y
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2d(self.x * other, self.y * other)
        return NotImplemented

    __rmul__ = __mul__

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __matmul__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return self.x * x + self.y * y
        return NotImplemented

    __rmatmul__ = __matmul__

    def __truediv__(self, other):  # self * (1 / other)
        return self.__mul__(1 / other)

    def __itruediv__(self, other):  # self /= other
        return self.__imul__(1 / other)

    # Comparações
    def __eq__(self, other):
        if isinstance(other, (Vec2d, tuple)):
            x, y = other
            return x == self.x and y == self.y
        return NotImplemented

    # Comportamento de sequências
    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, idx):
        return (self.x, self.y)[idx]

    def __setitem__(self, idx, value):
        if idx == 0:
            self.x = value
        elif idx == 1:
            self.y = value

    # Métodos da classe
    def copy(self):
        """
        Retorna cópia do vetor.
        """
        return Vec2d(self.x, self.y)

    def cross(self, other: VecLike) -> float:
        """
        Retorna componente z do produto vetorial com outro vetor.
        
        ``u.cross(v) -> u.x * v.y - u.y * v.x``
        """
        raise NotImplementedError

    def dot(self, other: VecLike) -> float:
        """
        Retorna o produto escalar com outro vetor.
        
        ``v1.dot(v2) -> v1.x*v2.x + v1.y*v2.y``
        """
        other = asvec2d(other)
        return self @ other

    def get_angle_between(self, other: VecLike) -> float:
        """
        Retorna ângulo entre self e outro vetor (em radianos).
        """
        other = asvec2d(other)
        cos_a = (self @ other) / self.length / other.length

        decimal = abs(cos_a -1)
        if cos_a > 0 and decimal < 1e-6:
            cos_a = 1
        elif cos_a < 0 and decimal < 1e-6:
            cos_a = -1
       
        return acos(cos_a)

    def get_angle_degrees_between(self, other: VecLike) -> float:
        """
        Retorna ângulo entre self e outro vetor (em graus).
        """
        return round(RADS_TO_DEGREES * self.get_angle_between(other)) 

    def get_dist_sqrd(self, other: VecLike) -> float:
        """
        Retorna o quadrado da distância entre self e outro vetor.
        """
        raise NotImplementedError

    def get_distance(self, other: VecLike) -> float:
        """
        Retorna a distância entre self e outro vetor.
        """
        return sqrt(self.get_dist_sqrd(other))

    def normalized(self) -> "Vec2d":
        """
        Retorna cópia normalizada do vetor.
        """
        raise NotImplementedError

    def normalize_return_length(self) -> float:
        """
        Normaliza vetor e retorna tamanho antes da normalização.
        """
        raise NotImplementedError

    def interpolate_to(self, other: VecLike, range: float) -> "Vec2d":
        """
        Interpola vetor até other no intervalo controlado por range.

        Range varia de forma que se range=0.0, retorna self, range=1.0 retorna other
        e valores intermediários produzem interpolações. 
        """
        raise NotImplementedError

    def perpendicular(self) -> "Vec2d":
        """
        Retorna vetor perpendicular na direção 90 graus anti-horário.
        """
        return Vec2d(-self.y, self.x)

    def perpendicular_normal(self) -> "Vec2d":
        """
        Retorna vetor normalizado e perpendicular na direção 90 graus anti-horário.
        """
        return self.perpendicular().normalized()

    def projection(self, other: VecLike) -> "Vec2d":
        """
        Projeta vetor em cima de outro vetor.
        """
        return ((self @ other) / other.length_sqrd) * other

    def rotate(self, angle: float):
        """
        Rotaciona vetor pelo ângulo em radianos.
        """
        _x = self.x * cos(angle) - self.y * sin(angle)
        _y = self.x * sin(angle) + self.y * cos(angle)

        self.x, self.y = (_x, _y)

    def rotate_degrees(self, angle: float):
        """
        Rotaciona vetor pelo ângulo em graus.
        """
        self.rotate(angle * DEGREES_TO_RADS)

    def rotated(self, angle: float) -> "Vec2d":
        """
        Cria novo vetor rotacionado ângulo em radianos.
        """
        rotated = self.copy()
        rotated.rotate(angle)
        return rotated

    def rotated_degrees(self, angle: float) -> "Vec2d":
        """
        Cria novo vetor rotacionado ângulo em graus.
        """
        return self.rotated(angle * DEGREES_TO_RADS)


#
# Funções auxiliares
#
def asvec2d(obj) -> "Vec2d":
    """
    Converte objeto para Vec2d, caso não seja vetor. 
    """
    if isinstance(obj, Vec2d):
        return obj
    elif isinstance(obj, tuple):
        x, y = obj
        return Vec2d(x, y)

    kind = type(obj).__name__  # Extrai nome do tipo de obj.
    raise TypeError(f"não pode converter {kind} em Vec2d")
