import pytest
from solution import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def complex_func(a: int, b: str, c: bool, d: float) -> str:
    return f"{a}{b}{c}{d}"


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (10, 20, 30),
    ]
)
def test_correct_types(a, b, expected):
    assert sum_two(a, b) == expected


@pytest.mark.parametrize(
    "a, b",
    [
        (1, 2.4),
        ("1", 2),
        (1, "2"),
    ]
)
def test_incorrect_types(a, b):
    with pytest.raises(TypeError):
        sum_two(a, b)


@pytest.mark.parametrize(
    "a, b, c, d, expected",
    [
        (1, "test", True, 3.14, "1testTrue3.14"),
    ]
)
def test_complex_func_correct(a, b, c, d, expected):
    assert complex_func(a, b, c, d) == expected


@pytest.mark.parametrize(
    "a, b, c, d",
    [
        (1, "test", "True", 3.14),
        (1.5, "test", True, 3.14),
    ]
)
def test_complex_func_incorrect(a, b, c, d):
    with pytest.raises(TypeError):
        complex_func(a, b, c, d)
