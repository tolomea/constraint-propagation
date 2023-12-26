from src.common import Solver
from src.common import get_user_input


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


if __name__ == "__main__":
    sudoku(get_user_input)
