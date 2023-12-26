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
    sudoku(get_input)


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
    sudoku(get_input)
