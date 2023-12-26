from src.common import Solver
from src.common import get_user_input


def format(cells):
    res = []
    for row in range(9):
        line = []
        for col in range(9):
            vals = cells[(row, col)]
            if len(vals) == 1:
                line.append(str(vals.pop()))
            else:
                line.append(".")
        res.append("".join(line))
    return res


def sudoku(get_input):
    solver = Solver()

    # get puzzle
    for row in range(9):
        line = get_input(
            f"Enter line {row + 1} use '.' for empty", pattern=r"[.1-9]{9}"
        )
        for col, c in enumerate(line):
            cell = (row, col)
            if c == ".":
                solver.set_cell(cell, set(range(1, 10)))
            else:
                solver.set_cell(cell, {int(c)})

    return format(solver.get_cells())


if __name__ == "__main__":
    res = sudoku(get_user_input)
    for row in res:
        print(row)  # noqa: T201
