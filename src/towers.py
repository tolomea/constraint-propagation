from src import latin_square
from src.common import get_canned_input
from src.common import get_user_input


def _all_possible_patterns(all_cells_values):
    first_cell_values, *remaining_cells_values = all_cells_values

    # deal with the rest of the problem
    if not remaining_cells_values:
        remaining_cells_patterns = [[]]  # only empty list
    else:
        remaining_cells_patterns = _all_possible_patterns(remaining_cells_values)

    # then add us onto the front
    for remaining_cells_pattern in remaining_cells_patterns:
        used_values = set(remaining_cells_pattern)
        for value in first_cell_values - used_values:
            yield [value] + remaining_cells_pattern


def _check_pattern_against_limit(limit, pattern):
    prev = float("-inf")
    count = 0
    for value in pattern:
        if value > prev:
            prev = value
            count += 1
    return count == limit


def constraint(start_limit, end_limit):
    def inner(all_cells_values: list[set[int]]) -> list[set[int]]:
        # filter to only the patterns that match the limits
        good_patterns = []
        for pattern in _all_possible_patterns(all_cells_values):
            if start_limit:
                if not _check_pattern_against_limit(start_limit, pattern):
                    continue
            if end_limit:
                if not _check_pattern_against_limit(end_limit, reversed(pattern)):
                    continue
            good_patterns.append(pattern)

        # flatten and return the result
        return [set(values) for values in zip(*good_patterns)]

    return inner


def towers(get_input):
    size = get_input("Puzzle size", convert=int)

    # get top limits
    top = get_input(
        "Enter top limits, start with a space, use space where there is no limit",
        pattern=rf" [ 1-{size}]{{0,{size}}}",
    )
    top += " " * size  # pad with spaces
    top = top[1:]  # drop leading space
    top = [int(top[i]) if top[i].strip() else None for i in range(size)]

    # get latin square body and side limits
    latin_square_input = []
    left = []
    right = []
    for row in range(size):
        start, middle, end = get_input(
            f"Enter line {row + 1} use '.' for empty, include the start and end"
            " limits, use space for no limit.",
            pattern=(
                rf"(?P<start>[ 1-{size}])"
                rf"(?P<middle>[.1-{size}]{{{size}}})"
                rf"(?P<end>[ 1-{size}]?)"
            ),
            groups=["start", "middle", "end"],
        )
        left.append(int(start) if start.strip() else None)
        latin_square_input.append(middle)
        right.append(int(end) if end.strip() else None)

    # get bottom limits
    bottom = get_input(
        "Enter bottom limits, start with a space, use space where there is no limit",
        pattern=rf" [ 1-{size}]{{0,{size}}}",
    )
    bottom += " " * size  # pad with spaces
    bottom = bottom[1:]  # drop leading space
    bottom = [int(bottom[i]) if bottom[i].strip() else None for i in range(size)]

    solver = latin_square.get_solver(size, get_canned_input(latin_square_input))

    for i in range(size):
        # add tower row constraints
        if left[i] or right[i]:
            solver.add_constraint(
                [(i, j) for j in range(size)], constraint(left[i], right[i])
            )
        # add tower col constraints
        if top[i] or bottom[i]:
            solver.add_constraint(
                [(j, i) for j in range(size)], constraint(top[i], bottom[i])
            )

    if solution := solver.solve():
        return latin_square.format(size, solution.get_cells())

    return []


if __name__ == "__main__":
    res = towers(get_user_input)
    for row in res:
        print(row)  # noqa: T201
