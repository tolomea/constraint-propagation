from src.common import get_canned_input
from src.towers import towers


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
    res = towers(get_input)
    print(res)  # noqa: T201
    assert res == [
        # force black to split lines
        "12534",
        "54213",
        "41325",
        "23451",
        "35142",
    ]


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
    res = towers(get_input)
    print(res)  # noqa: T201
    assert res == [
        # force black to split lines
        "416253",
        "654132",
        "325461",
        "562314",
        "143625",
        "231546",
    ]


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
    res = towers(get_input)
    print(res)  # noqa: T201
    assert res == [
        # force black to split lines
        "416253",
        "654132",
        "325461",
        "562314",
        "143625",
        "231546",
    ]
