from src import latin_square
from src.common import get_user_input


def sudoku(get_input):
    solver = latin_square.get_solver(9, get_input)

    # add block constraints
    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            solver.add_constraint(
                [(i + k, j + l) for k in [0, 1, 2] for l in [0, 1, 2]],
                latin_square.constraint,
            )

    if solution := solver.solve():
        return latin_square.format(9, solution.get_cells())

    return []


if __name__ == "__main__":
    res = sudoku(get_user_input)
    for row in res:
        print(row)  # noqa: T201
