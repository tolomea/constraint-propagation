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
    assert res == ["12345", "21453", "34512", "45231", "53124"]


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
    assert res == ["124356", "215463", "341625", "436512", "563241", "652134"]


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
    assert res == ["124356", "215463", "341625", "436512", "563241", "652134"]
