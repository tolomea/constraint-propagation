import pytest

from src.common import Inconsistent
from src.common import get_test_input
from src.sudoku import constraint
from src.sudoku import sudoku


def test_basic():
    get_input = get_test_input(
        [
            ".48326.19",
            "....5..72",
            "2597.8.46",
            "8.5.43...",
            "...8.1..4",
            ".1....2..",
            ".87...6.5",
            "....3...8",
            "1.26..4..",
        ]
    )
    res = sudoku(get_input)
    print(res)  # noqa: T201
    assert res == [
        "748326519",
        "361954872",
        "259718346",
        "875243961",
        "923861754",
        "614579283",
        "487192635",
        "596437128",
        "132685497",
    ]


def test_expert():
    get_input = get_test_input(
        [
            "..4..8..6",
            "..52..18.",
            ".1......7",
            "..2.9....",
            "........1",
            ".5...734.",
            "4..7.....",
            ".3...485.",
            ".......6.",
        ]
    )
    res = sudoku(get_input)
    print(res)  # noqa: T201
    assert res == [
        "..41785.6",
        "..524.189",
        ".1...94.7",
        "..2.91675",
        "......291",
        ".5.627348",
        "4..7..913",
        ".3.9.4852",
        "5.....764",
    ]


def test_invalid():
    get_input = get_test_input(
        [
            ".44..8..6",
            "..52..18.",
            ".1......7",
            "..2.9....",
            "........1",
            ".5...734.",
            "4..7.....",
            ".3...485.",
            ".......6.",
        ]
    )
    with pytest.raises(Inconsistent):
        sudoku(get_input)


def test_constraint_only():
    res = constraint([{1, 2, 3, 4}, {2, 3, 4}, {2, 3, 4}, {2, 3, 4}])
    assert res == [{1}, {2, 3, 4}, {2, 3, 4}, {2, 3, 4}]


def test_constraint_basic():
    res = constraint([{1}, {1, 2, 3, 4}, {1, 2, 3, 4}, {3}])
    assert res == [{1}, {2, 4}, {2, 4}, {3}]


def test_constraint_double():
    res = constraint([{1, 2, 3, 4}, {1, 2}, {1, 2}, {1, 2, 3, 4}])
    assert res == [{3, 4}, {1, 2}, {1, 2}, {3, 4}]


def test_constraint_triple():
    res = constraint([{1, 2}, {2, 3}, {1, 3}, {1, 2, 3, 4}])
    assert res == [{1, 2}, {2, 3}, {1, 3}, {4}]


def test_constraint_overlap_up():
    res = constraint([{1, 2}, {1, 2, 3}, {3}, {1, 2, 3, 4}])
    assert res == [{1, 2}, {1, 2}, {3}, {4}]


def test_constraint_overlap_down():
    res = constraint([{1, 2}, {1, 2}, {1, 2, 3}, {1, 2, 3, 4}])
    assert res == [{1, 2}, {1, 2}, {3}, {4}]
