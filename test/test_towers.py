from src.towers import towers
from src.common import get_canned_input


def test_basic():
    get_input = get_canned_input(
        [
            # force black to split lines
            "5",
            " 23122",
            "3.....2",
            "1.....3",
            "2.....1",
            "4.....2",
            "2.....3",
            " 31322",
        ]
    )
    towers(get_input)


def test_expert():
    get_input = get_canned_input(
        [
            "6",
            "   13 4",
            "2......",
            " ......5",
            "3......",
            "2......2",
            "3..3...",
            " ......",
            " 3 42",
        ]
    )
    towers(get_input)


def test_expert_padded():
    get_input = get_canned_input(
        [
            "6",
            "   13 4",
            "2...... ",
            " ......5",
            "3...... ",
            "2......2",
            "3..3... ",
            " ...... ",
            " 3 42  ",
        ]
    )
    towers(get_input)
