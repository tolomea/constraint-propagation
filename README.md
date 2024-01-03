# Let's use constraint propagation to solve some problems.

These problems will all have the following properties:

1. There are a number of squares, lets call them cells since they are not always squares.
2. Each can have one and only one correct value and the goal is to find those correct values.
4. There are a number of constraints that limit what values the cells can take on.
5. All information is available at the start.
6. Additionally at the start we may already have the final values for some cells.

# Sudoku

As a concrete example lets consider Sudoku.
1. It's played on a 9x9 grid of 81 cells
1. Each cell will have a value between 1 and 9 and we need to find those values.
1. There are 3 rules that limit what values cells can take on:
   1. The values 1-9 may appear only once in each row.
   1. The values 1-9 may appear only once in each column.
   1. If we divide the 9x9 gird into a 3x3 grid of 3x3 blocks then the values 1-9 may appear only once in each block.

(These could be viewed as the same constraint applied to differing sets of cells).

## I/O

We're going to need some interaction with the user, so they can describe the problem to us and we can tell them the solution.

### Input

To make this easier I have made a wrapper around the builtin `input` that can also do some validation.
We're going to pass this into the specific problems dependency injection style as that will make testing easier.

To read in a Sudoku puzzle will look something like:
```
def sudoku(get_input):
    for row in range(1, 10):
        line = get_input(f"Enter row {row}, use '.' for empty", pattern=r"[.0-9]{9}")
        # do stuff with line
```

### Solver Creation

We're going to have a general solver which will be used with all the problems.
The solver doesn't need to be aware of size or shape of the problem, all it really needs to know is:
1. What cells are there
2. What are their possible values
3. What constraints exist over what cells

We're going to treat a cell "name" as anything that can be used as a dictionary key.
And the values are going to be anything that can be put in a set.
For Sudoku the names are going to be `(row, col)` tuples and the values integers.

Extending the above to create a solver and pass it the initial values would look like:
To read in a Sudoku puzzle will look something like:
```
def sudoku(get_input):
    solver = Solver()
    for row in range(1, 10):
        line = get_input(f"Enter line {i} use '.' for empty", pattern=r"[.0-9]{9}")
        for col, c in enumerate(line, start=1):
            cell = (row, col)
            if c == ".":
                solver.set_cell(cell, set(range(1, 10)))
            else:
                solver.set_cell(cell, {int(c)})
```

### Output

We also want to be able to print it back to make sure it was loaded ok.
```
def format(cells):
    res = []
    for row in INTS:
        line = []
        for col in INTS:
            vals = cells[(row, col)]
            if len(vals) == 1:
                line.append(str(vals.pop()))
            else:
                line.append(".")
        res.append("".join(line))
    return res
```

## Constraints

Next we need to explain the constraints to the Solver. For the Solver a constraint consists of two essential things:
1. A set of cells the constraint applies to.
2. A function which takes the current possible values for those cells and returns the new (hopefully reduced) possible values.

For Sudoku the constraint is that "each number appears once and only once within the associated cells".
We need to break this out into the two directions and express it in a way that dictates the values of the cells.

### One value per cell

First "if a value can only be in one cell then nothing else can be in that cell"
```
    for v in range(1, 10):
        indexes = [i for i, values in enumerate(all_cells_values) if v in values]
        if len(indexes) == 1:
            (index,) = indexes
            all_cells_values[index] = {v}

```

### Once cell per value

And then "if a particular value has to be in once cell then it can't be in any other cell".
```
    for i, cell_values in enumerate(all_cells_values):
        if len(cell_values) == 1:
            (cell_value,) = cell_values
            # used, so remove from all others
            for j, other_cell_values in enumerate(all_cells_values):
                if j != i:
                    other_cell_values.discard(cell_value)
```

### N cells for N values

However consider the case where two cells can both be either 1 or 2 but nothing else, this tells us none of the other cells can be 1 or 2.
Likewise if one cell can be 1 or 2, another 2 or 3 and a third 1 or 3. Then those 3 cells have "covered" the values 1, 2 and 3 and those values can't appear in the other cells.
So our second statement above can be broadened to "if N cells can only contain N values then those values can't be in any of the other cells".
That might look like:
```
    for cells in all_subsets(range(len(all_cells_values))):
        cells_values = set()
        for cell in cells:
            cells_values |= all_cells_values[cell]
        if len(cells_values) == len(cells):
            # used, so remove from all others
            for other_cell, other_cell_values in enumerate(all_cells_values):
                if other_cell not in cells:
                    other_cell_values -= cells_values

```

### Construction

Next we need to tell the solver about the constraints.

```
    # add constraints
    for i in INTS:
        solver.add_constraint([(i, j) for j in INTS], constraint)
        solver.add_constraint([(j, i) for j in INTS], constraint)

    for i in [1, 4, 7]:
        for j in [1, 4, 7]:
            solver.add_constraint(
                [(i + k, j + l) for k in [0, 1, 2] for l in [0, 1, 2]], constraint
            )
```

## Wrapup

We're about done with Sudoku, the only thing left is a little solve and print:
```
    solver.solve()

    return format(solver.get_cells())
```

# Solving

Which brings us around to the question of what magic is the solver doing?

## Book keeping

First there's the book keeping for the stuff we've given it.
```
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

```

## Propagation

The core constraint propagation algorithim is quite straight forward.
0: put all the constraints in a queue
1: take a constraint off the queue
2: fetch the values for it's cells
3: call the constraint to evaluate the cells values
4: check the new cell values against the existing ones
5: if a cells values changed update them and add any constraints for that cell to the queue
6: repeat until the queue is empty
```
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
                    self.cells[cell] = new
                    queue.update(self.cell_constraints[cell])
        return
```

## Recursive guessing

This alone is enough to solve easy problems.
However it cannot solve problems requiring advanced techniques like XY Wing.
Fundamentally these advanced techniques rely on evaluating multiple constraints together.
We could code up systems for this... or we could guess.
The constraint propagation is doing most of the heavy lifting, we just need a way to break out of complex deadends.
A guess, test and backtrack setup could do this.
For this we need a way to copy the current state:
```
    def copy(self):
        new_solver = Solver()
        new_solver.cells = {k: set(vals) for k, vals in self.cells.items()}
        new_solver.constraint_cells = list(self.constraint_cells)
        new_solver.constraint_funcs = list(self.constraint_funcs)
        new_solver.cell_constraints = {
            k: set(vals) for k, vals in self.cell_constraints.items()
        }
        return new_solver
```

A way to test if we're done:
```
    def is_done(self):
        return all(len(v) == 1 for v in self.cells.values())
```

And then the basic plan is
0: propagate
1: if that fails return None
2: if we're done return
3: otherwise try guesses on copies
4: if one works return
5: otherwise return None
```
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
```

## Wrapup

And a small update to the main Sudoku function:
```
    if solution := solver.solve():
        return format(solution.get_cells())

    return []
```

And that's it, Sudoku solved.

# Towers

I know of towers from [Simon Tatham's Portable Puzzle Collection](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/)
![Towers game image](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/towers-web.png)

The basic idea is you have a gird of size N.
Each cell in the grid gets a number 1-N.
So far a bit like Sudoku but without the sub blocks, this general pattern is called a Latin Square.
The numbers indicate the height of the tower in that square, when looking from the side a tall tower hides a lower one.
Some rows and columns have numbers at one or both ends saying how many towers are visible from that location.

## Latin Squares

First up lets pull out this idea of a Latin Square into a helper.
There's no new code to that, it's mostly moving half of sudoku.py to a new file.
It exposes one main function `get_solver` which takes a size and an input function and returns a solver pre-initilized with the latin square row and column constraints and possible values for each cell.

## I/O

### Input

The size of this puzzle is variable, it will be easier if we just ask up front what size it is.
Then we just need to read it all in.
```
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
        )
        starts.append(start)
        latin_square_input.append(middle)
        ends.append(end)
    bottom = get_input(
        "Enter bottom limits, start with a space, use space where there is no limit",
        pattern=rf" [ 1-{size}]{{0,{size}}}",
    )
```

### Solver Creation and Output

And then hook it up to the latin square, solve and print.

```
    solver = latin_square.get_solver(size, get_canned_input(latin_square_input))

    if solution := solver.solve():
        return latin_square.format(size, solution.get_cells())

    return []
```

It works at this point because the latin square code can find a valid solution. But it's not a towers solution because we are missing the towers constraints.
