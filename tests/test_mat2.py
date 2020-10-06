"""
Módulo de testes para a classe Mat2. 

Utiliza os vetores u = <3,4>, v = <1,1>, ii=<1,0> e jj=<0,1> e as matrizes

M = |1 2|
    |3 4|

N = | 1 -1|
    |-1  1|

II = |1 0|
     |0 1|

definidos em conftest.
"""
import pytest
import random
from math import pi, sqrt
from pytaon import Mat2, Vec2d


def similar(x, y, tol=1e-6):
    if isinstance(x, Mat2):
        (u, v) = x - y
        assert abs(u) <= tol and abs(v) <= tol
    return abs(x - y) <= tol


class TestMat2:
    def test_matrix_attributes(self, M):
        assert M.a == 1
        assert M.b == 3
        assert M.c == 2
        assert M.d == 4
        assert M.trace == 5
        assert M.determinant == -2
        assert M.T.T == M

    def test_matrix_invariants(self, M):
        assert M.T.T == M
        assert M.copy() == M
        assert M.rotated(0.0) == M
        assert M.rotated_degrees(0.0) == M

    def test_neg_and_pos(self, u):
        assert (-u) == u * (-1)
        assert (+u) == u * (+1)
        assert +u is not u

    def test_sum(self, M, N):
        assert M + N == Mat2(2, 2, 1, 5)
        assert M + Mat2.zero() == M
        assert Mat2.zero() + Mat2.zero() == Mat2.zero()

    def test_sub(self, M, N):
        assert M - N == Mat2(0, 4, 3, 3)
        assert M - Mat2.zero() == M
        assert Mat2.zero() - Mat2.zero() == Mat2.zero()

    def test_div(self, M):
        assert M / 1 == M
        assert (M / 2).trace == M.trace / 2
        assert M / 2 == M * 0.5

        MM = M / 2
        assert MM.a == M.a / 2
        assert MM.b == M.b / 2
        assert MM.c == M.c / 2
        assert MM.d == M.d / 2

    def test_prod_with_number(self, M):
        assert M * 1 == 1 * M == M
        assert (M * 2).trace == 2 * M.trace
        assert M * 2 == 2 * M

        MM = M * 2
        assert MM.a == 2 * M.a
        assert MM.b == 2 * M.b
        assert MM.c == 2 * M.c
        assert MM.d == 2 * M.d

    def test_prod(self, M, N, II):
        assert M * N == Mat2(-1, -1, 1, 1)
        assert M * II == M
        assert II * M == M

    def test_prod_with_vec(self, M, II, u):
        assert M * u == M.transform_vector(u)
        assert u * M == M.T.transform_vector(u)
        assert II * u == u
        assert u * II == u

    def test_inplace_operations(self, M, N):
        M_ref = M
        MM = M.copy()

        M += N
        assert M.trace == MM.trace + N.trace
        assert M is M_ref

        M -= N
        assert M.trace == MM.trace
        assert M == MM
        assert M is M_ref

        M *= 2
        assert M.trace == 2 * MM.trace
        assert M is M_ref

        M /= 2
        assert M.trace == MM.trace
        assert M == MM
        assert M is M_ref

    def test_item_getter_1d(self, M, N, II):
        for m in [M, N, II]:
            assert m[0] == (m.a, m.c)
            assert m[1] == (m.b, m.d)

    def test_item_getter_2d(self, M, N, II):
        for m in [M, N, II]:
            assert m[0, 0] == m.a
            assert m[1, 0] == m.b
            assert m[0, 1] == m.c
            assert m[1, 1] == m.d

    def test_item_setter(self, M):
        M[0, 0] = a = random.random()
        M[1, 0] = b = random.random()
        M[0, 1] = c = random.random()
        M[1, 1] = d = random.random()
        assert M.a == a
        assert M.b == b
        assert M.c == c
        assert M.d == d

    def test_item_raises_index_error(self, M):
        with pytest.raises(IndexError):
            print(M[2])
        with pytest.raises(IndexError):
            M[2] = 0.0
        with pytest.raises(IndexError):
            print(M[1, 2])
        with pytest.raises(IndexError):
            M[1, 2] = 0.0
        with pytest.raises(IndexError):
            print(M[0, 0])

    def test_interpolate_to(self, M, N):
        assert similar(M.interpolate_to(N, 0), M)
        assert similar(M.interpolate_to(N, 1), N)
        assert similar(M.interpolate_to(N, 0.5), (M + N) / 2)

    def test_rotate(self, M):
        MM = M.copy()
        det = M.determinant
        rotation = pi * random.random()
        assert M.rotate(rotation) is None
        assert similar(M.determinant, det)

        M.rotate(-rotation)
        assert similar(M, MM)

    def test_rotated(self, M):
        rotation = pi * random.random()
        MM = M.rotated(rotation)
        assert similar(MM.determinant, M.determinant)
        assert similar(MM.rotated(-rotation), M)
