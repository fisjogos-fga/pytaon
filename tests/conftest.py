import sys
from pathlib import Path
import pytest

PATH = Path(__file__).parent.parent
sys.path.append(str(PATH))

from pytaon import Mat2, Vec2d


@pytest.fixture
def u():
    return Vec2d(3, 4)


@pytest.fixture
def v():
    return Vec2d(1, 1)


@pytest.fixture
def ii():
    return Vec2d(1, 0)


@pytest.fixture
def jj():
    return Vec2d(0, 1)


@pytest.fixture
def M():
    return Mat2(1, 3, 2, 4)


@pytest.fixture
def N():
    return Mat2(1, -1, -1, 1)


@pytest.fixture
def II():
    return Mat2(1, 0, 0, 1)
