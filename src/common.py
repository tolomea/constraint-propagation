import re


def get_user_input(prompt, pattern=None, convert=None):
    while True:
        value = input(f"{prompt}: ")
        if not value:
            continue
        if pattern:
            if not re.fullmatch(pattern, value):
                print(f"Does not match '{pattern}'")  # noqa: T201
                continue
        if convert:
            try:
                value = convert(value)
            except Exception as e:
                print(e)  # noqa: T201
                continue
        return value


def get_test_input(lines):
    lines = list(lines)

    def inner(prompt, pattern=None, convert=None):
        value = lines.pop(0)
        if pattern:
            assert re.fullmatch(pattern, value), (pattern, value)
        if convert:
            value = convert(value)
        return value

    return inner


class Solver:
    def __init__(self):
        self.cells = {}
        self.constraint_cells = []
        self.constraint_funcs = []
        self.cell_constraints = {}

    def set_cell(self, name, values):
        self.cells[name] = set(values)
        if name not in self.cell_constraints:
            self.cell_constraints[name] = set()

    def get_cells(self):
        return {key: set(val) for key, val in self.cells.items()}

    def add_constraint(self, cells, constraint_func):
        index = len(self.constraint_cells)
        assert index == len(self.constraint_funcs)
        self.constraint_cells.append(list(cells))
        self.constraint_funcs.append(constraint_func)
        for cell in cells:
            self.cell_constraints.setdefault(cell, set()).add(index)
