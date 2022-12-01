import pytest
from app.calculations import add, subtract, multiply, divide


@pytest.mark.parametrize()
def test_Add():
    print("Testing add function")
    assert add(5, 3) == 8


def test_subtract():
    assert subtract(10, 3) == 7


def test_divide():
    assert divide(81, 3) == 27


def test_multiply():
    assert multiply(4, 8) == 32
