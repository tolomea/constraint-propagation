from src import latin_square
from src.common import get_user_input, get_canned_input


def towers(get_input):
    size = get_input("Puzzle size", convert=int)

    top = get_input(
        "Enter top limits, start with a space, use space where there is no limit",
        pattern=rf" [ 1-{size}]{{0,{size}}}",
    )

    latin_square_input = []
    starts = []
    ends = []

    for row in range(size):
        start, middle, end = get_input(
            f"Enter line {row + 1} use '.' for empty, include the start and end limits,"
            " use space for no limit.",
            pattern=(
                rf"(?P<start>[ 1-{size}])"
                rf"(?P<middle>[.1-{size}]{{{size}}})"
                rf"(?P<end>[ 1-{size}]?)"
            ),
            groups=["start", "middle", "end"],
        )
        starts.append(start)
        latin_square_input.append(middle)
        ends.append(end)

    bottom = get_input(
        "Enter bottom limits, start with a space, use space where there is no limit",
        pattern=rf" [ 1-{size}]{{0,{size}}}",
    )


if __name__ == "__main__":
    res = towers(get_user_input)
    for row in res:
        print(row)  # noqa: T201
