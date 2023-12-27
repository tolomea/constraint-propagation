from itertools import chain
from itertools import combinations

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


def all_subsets(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def constraint(all_cells_values: list[set[int]]) -> list[set[int]]:
    # if a number can only be in one place then nothing else can be there
    for v in range(1, 10):
        indexes = [i for i, values in enumerate(all_cells_values) if v in values]
        if len(indexes) == 1:
            (index,) = indexes
            all_cells_values[index] = {v}

    # if we know where a number must be then it can't be anywhere else
    for cells in all_subsets(range(len(all_cells_values))):
        cells_values = set()
        for cell in cells:
            cells_values |= all_cells_values[cell]
        if len(cells_values) == len(cells):
            # used, so remove from all others
            for other_cell, other_cell_values in enumerate(all_cells_values):
                if other_cell not in cells:
                    other_cell_values -= cells_values

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

    # add constraints
    for i in range(9):
        solver.add_constraint([(i, j) for j in range(9)], constraint)
        solver.add_constraint([(j, i) for j in range(9)], constraint)

    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            solver.add_constraint(
                [(i + k, j + l) for k in [0, 1, 2] for l in [0, 1, 2]], constraint
            )

    if solution := solver.solve():
        return format(solution.get_cells())

    return []


if __name__ == "__main__":
    res = sudoku(get_user_input)
    for row in res:
        print(row)  # noqa: T201
