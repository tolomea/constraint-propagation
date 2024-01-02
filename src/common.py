import re


def parse_line(value, pattern, convert):
    if pattern:
        if not re.fullmatch(pattern, value):
            raise Exception(f"Does not match '{pattern}'")
    if convert:
        value = convert(value)
    return value


def get_user_input(prompt, pattern=None, convert=None):
    while True:
        value = input(f"{prompt}: ")
        if not value:
            continue
        try:
            value = parse_line(value, pattern=pattern, convert=convert)
        except Exception as e:
            print(e)  # noqa: T201
            continue
        else:
            return value


def get_canned_input(lines):
    lines = list(lines)

    def inner(prompt, pattern=None, convert=None):
        value = lines.pop(0)
        try:
            return parse_line(value, pattern=pattern, convert=convert)
        except Exception:
            print(value)  # noqa: T201
            raise

    return inner


class Inconsistent(Exception):
    pass


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

    def propagate(self):
        # put all the constraints in the queue
        queue = set(range(len(self.constraint_cells)))

        while queue:
            index = queue.pop()
            cells = self.constraint_cells[index]
            values = [self.cells[cell] for cell in cells]

            new_values = self.constraint_funcs[index]([set(vals) for vals in values])
            for cell, old, new in zip(cells, values, new_values):
                if new != old:
                    if not new:  # ran out of options, something is wrong
                        raise Inconsistent()
                    self.cells[cell] = new
                    queue.update(self.cell_constraints[cell])
        return

    def copy(self):
        new_solver = Solver()
        new_solver.cells = {k: set(vals) for k, vals in self.cells.items()}
        new_solver.constraint_cells = list(self.constraint_cells)
        new_solver.constraint_funcs = list(self.constraint_funcs)
        new_solver.cell_constraints = {
            k: set(vals) for k, vals in self.cell_constraints.items()
        }
        return new_solver

    def is_done(self):
        return all(len(v) == 1 for v in self.cells.values())

    def solve(self):
        try:
            self.propagate()
        except Inconsistent:
            return None

        if self.is_done():
            return self

        for cell, values in self.cells.items():
            if len(values) > 1:
                for value in values:
                    new_solver = self.copy()
                    new_solver.cells[cell] = {value}
                    if result := new_solver.solve():
                        return result

        return None
