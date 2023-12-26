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


def constraint(all_cells_values: list[set[int]]) -> list[set[int]]:
    # if a number can only be in one place then nothing else can be there
    for v in range(1, 10):
        indexes = [i for i, values in enumerate(all_cells_values) if v in values]
        if len(indexes) == 1:
            (index,) = indexes
            all_cells_values[index] = {v}

    # if we know where a number must be then it can't be anywhere else
    for i, cell_values in enumerate(all_cells_values):
        if len(cell_values) == 1:
            (cell_value,) = cell_values
            # used, so remove from all others
            for j, other_cell_values in enumerate(all_cells_values):
                if j != i:
                    other_cell_values.discard(cell_value)

    return all_cells_values


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
