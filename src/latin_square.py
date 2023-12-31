from itertools import chain
from itertools import combinations

from src.common import Solver


def format(size, cells):
    res = []
    for row in range(size):
        line = []
        for col in range(size):
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
    all_values = set()
    for cell_values in all_cells_values:
        all_values.update(cell_values)

    # if a number can only be in one place then nothing else can be there
    for v in all_values:
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


def get_solver(size, get_input):
    """
    Make a latin square with inidicies 0 to size-1 with potential values 1 to size
    """

    solver = Solver()

    # get puzzle
    for row in range(size):
        line = get_input(
            f"Enter line {row + 1} use '.' for empty", pattern=rf"[.1-{size}]{{{size}}}"
        )
        for col, c in enumerate(line):
            cell = (row, col)
            if c == ".":
                solver.set_cell(cell, set(range(1, size + 1)))
            else:
                solver.set_cell(cell, {int(c)})

    # add constraints
    for i in range(size):
        solver.add_constraint([(i, j) for j in range(size)], constraint)
        solver.add_constraint([(j, i) for j in range(size)], constraint)

    return solver
