"""
Módulo de testes para a classe Vec2d. 

Utiliza os vetores u = <3,4>, v = <1,1>, ii=<1,0> e jj=<0,1> definidos em conftest.
"""
import pytest
import random
from math import pi, sqrt
from pytaon import Vec2d


def similar(x, y, tol=1e-6):
    return abs(x - y) <= tol


class TestVec2d:
    def test_angle(self, u, v):
        assert u.angle > v.angle
        assert similar(u.angle, pi / 4)
        assert similar(u.angle_degrees, 45)

    def test_angle_setter(self, u, v):
        u.angle = 0.0
        assert similar(u.x, 5.0)
        assert similar(u.y, 0.0)

        u.angle_degrees = 45.0
        assert similar(u.x, 2.5 * sqrt(2))
        assert similar(u.y, 2.5 * sqrt(2))

        u.angle = pi / 4
        assert similar(u.x, 2.5 * sqrt(2))
        assert similar(u.y, 2.5 * sqrt(2))

    def test_length(self, u, v):
        assert u.length > v.length
        assert u.length == 5
        assert u.length_sqrd == 25

    def test_length_setter(self, u):
        x, y = u
        u.length *= 2
        assert similar(u.x, 2 * x)
        assert similar(u.y, 2 * y)

    def test_algebraic_operations(self, u, v):
        assert u + v == Vec2d(u.x + v.x, u.y + v.y)
        assert u - v == Vec2d(u.x - v.x, u.y - v.y)
        assert u * 2 == Vec2d(2 * u.x, 2 * u.y)
        assert 2 * u == Vec2d(2 * u.x, 2 * u.y)
        assert u / 2 == Vec2d(u.x / 2, u.y / 2)

    def test_algebraic_operations_with_tuples(self, u, v):
        U, V = map(tuple, (u, v))
        assert u + v == u + V == U + v
        assert u - v == u - V == U - v

    def test_neg_and_pos(self, u):
        assert (-u) == u * (-1)
        assert (+u) == u * (+1)
        assert +u is not u

    def test_inplace(self, u):
        u_orig = u

        u += (1, 1)
        assert u == Vec2d(4, 5)
        assert u is u_orig

        u -= (1, 1)
        assert u == Vec2d(3, 4)
        assert u is u_orig

        u *= 2
        assert u == Vec2d(6, 8)
        assert u is u_orig

        u /= 2
        assert u == Vec2d(3, 4)
        assert u is u_orig

    def test_item_getter(self, u, v):
        for u in [u, v]:
            assert u[0] == u.x
            assert u[1] == u.y

    def test_item_setter(self, u):
        u[0] = n = random.random()
        u[1] = m = random.random()
        assert u.x == n
        assert u.y == m

    def test_item_raises_index_error(self, u):
        with pytest.raises(IndexError):
            u[2]
        with pytest.raises(IndexError):
            u[2] = 0.0

    def test_cross_product(self, u, v):
        V = tuple(v)
        assert similar(u.cross(v), -v.cross(u))
        assert similar(u.cross(v), -1)
        assert u.cross(v) == u.cross(V)

    def test_dot_product(self, u, v):
        V = tuple(v)
        assert u.dot(v) == 7.0
        assert u.dot(v) == u.dot(V)

    def test_get_angle_between(self, ii, v):
        II = tuple(ii)

        assert v.get_angle_between(v) == 0.0
        assert similar(v.get_angle_between((-1) * v), pi)

        assert v.get_angle_degrees_between(v) == 0.0
        assert similar(v.get_angle_degrees_between((-1) * v), 180)

        assert v.get_angle_between(ii) == v.get_angle_between(II)
        assert similar(v.get_angle_between(ii), pi / 4)
        assert similar(v.get_angle_degrees_between(ii), 45)

    def test_get_distance(self, u, v):
        assert similar(u.get_distance(v), sqrt(u.get_dist_sqrd(v)))
        assert similar(u.get_distance(v), sqrt(13))
        assert similar(u.get_dist_sqrd(v), 13)

    def test_get_distance_accepts_tuples(self, u, v):
        U, V = map(tuple, (u, v))

        assert similar(u.get_distance(v), u.get_distance(V))
        assert similar(u.get_dist_sqrd(v), u.get_dist_sqrd(V))

    def test_normalized(self, u):
        assert similar(u.normalized().length, 1)
        assert similar(u.normalized().angle, u.angle)

    def test_normalized_return_length(self, u):
        angle, length = u.angle, u.length
        assert similar(u.normalize_return_length(), length)
        assert similar(u.angle, angle)

    def test_interpolate_to(self, u, v):
        assert similar(u.interpolate_to(v, 0), u)
        assert similar(u.interpolate_to(v, 1), v)
        assert similar(u.interpolate_to(v, 0.5), (u + v) / 2)

    def test_interpolate_to_accept_tuples(self, u, v):
        V = tuple(v)
        assert similar(u.interpolate_to(v, 0.5), u.interpolate_to(V, 0.5))

    def test_perpendicular(self, u):
        v = u.perpendicular()
        assert similar(u.length, v.length)
        assert similar(u.dot(v), 0)
        assert similar(u.angle_between(v), pi / 2)

    def test_perpendicular_normal(self, u, v):
        v = u.perpendicular()
        assert similar(v.length, 1)
        assert similar(u.dot(v), 0)
        assert similar(u.angle_between(v), pi / 2)

    def test_projection(self, u, v):
        proj = u.projection(v)
        assert similar(proj.angle, v.angle)
        assert proj.length <= u.length
        assert similar(v.length * proj.length, u.dot(v))
        assert similar(u.length * v.projection(u).length, u.dot(v))

    def test_rotate(self, u):
        angle, length = u.angle, u.length
        rotation = pi * random.random()
        assert u.rotate(rotation) is None
        assert similar(u.angle, angle + rotation)
        assert similar(u.length, length)

    def test_rotated(self, u):
        rotation = pi * random.random()
        u_ = u.rotated(rotation)
        assert similar(u_.angle, u.angle + rotation)
        assert similar(u_.length, u.length)
