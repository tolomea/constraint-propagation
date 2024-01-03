from src.common import get_test_input
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
        "294178536",
        "375246189",
        "618539427",
        "842391675",
        "763485291",
        "951627348",
        "486752913",
        "137964852",
        "529813764",
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
    res = sudoku(get_input)
    print(res)  # noqa: T201
    assert res == []
