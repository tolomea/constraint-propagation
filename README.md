# constraint-propagation
Let's use constraint propagation to solve some problems.

These problems will all have the following properties:

1. There are a number of squares, lets call them cells since they are not always squares.
2. Each can have one and only one correct value and the goal is to find those correct values.
4. There are a number of constraints that limit what values the cells can take on.
5. All information is available at the start.
6. Additionally at the start we may already have the final values for some cells.


As a concrete example lets consider Sudoku.
1. It's played on a 9x9 grid of 81 cells
2. Each cell will have a value between 1 and 9 and we need to find those values.
3. There are 3 rules that limit what values cells can take on:
3.1. The values 1-9 may appear only once in each row.
3.2. The values 1-9 may appear only once in each column.
3.3. If we divide the 9x9 gird into a 3x3 grid of 3x3 blocks then the values 1-9 may appear only once in each block.
(These could be viewed as the same constraint applied to differing sets of cells).

We're going to need some input from the user, so they can describe the problem to us.
To make this easier I have made a wrapper around the builtin `input` that can also do some validation.
We're going to pass this into the specific problems dependency injection style as that will make testing easier.

To read in a Sudoku puzzle will look something like:
```
def sudoku(get_input):
    for row in range(1, 10):
        line = get_input(f"Enter row {row}, use '.' for empty", pattern=r"[.0-9]{9}")
        # do stuff with line
```


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

Next we need to explain the constraints to the Solver. For the Solver a constrain consists of two essential things:
1. A set of cells the constraint applies to.
2. A function which takes the current possible values for those cells and returns the new (hopefully reduced) possible values.

For Sudoku the constraint is that "a value can only appear once within the associated cells".
We need to reframe this so that it tell us about the other cells.
"If a value must appear in once cell then it can't appear in any of the others."
That might look like:

```
def constraint(all_cells_possible_values: list[set[int]]) -> list[set[int]]:
    for i, cell_possible_values in enumerate(all_cells_possible_values):
        if len(cell_possible_values) == 1:
            (cell_possible_value,) = cell_possible_values
            # used, so remove from all others
            for j, other_cell_possible_values in enumerate(all_cells_possible_values):
                if j != i:
                    other_cell_possible_values.discard(cell_possible_value)
    return all_cells_possible_values
```
