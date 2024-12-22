import dataclasses
import enum
import pathlib


def get_input(demo=True):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    res = []

    for row, i in enumerate(inp):
        cell_row = []
        for col, j in enumerate(i):
            if str(j).isdigit():
                cell = Cell(row=row, col=col, value=j, cell_type=CellType.Number)
            elif j == '.':
                cell = Cell(row=row, col=col, value=j, cell_type=CellType.Empty)
            else:
                cell = Cell(row=row, col=col, value=j, cell_type=CellType.Symbol)
            if j == '^':
                cell.guard = GuardType.GuardUp
            cell_row.append(cell)
        res.append(cell_row)
    return Grid(res)


class CellType(enum.Enum):
    Empty = enum.auto()
    Number = enum.auto()
    Symbol = enum.auto()


class GuardType(enum.Enum):
    GuardUp = [0, [-1, 0], '^']
    GuardRight = [1, [0, 1], '>']
    GuardDown = [2, [1, 0], 'v']
    GuardLeft = [3, [0, -1], '<']

    def get_next(self):
        next = (self.value[0] + 1) % 4
        for en in GuardType:
            if en.value[0] == next:
                return en

@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    row: int
    col: int
    value: ""
    cell_type: CellType.Empty


class Grid:
    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        return "\n".join(["".join([str(cell.value) for cell in row]) for row in self.grid])

    def get_cell(self, row, col) -> Cell:
        rows = len(self.grid)
        if row >= rows or row < 0:
            return None
            # row = row - rows
        cols = len(self.grid[row])
        if col >= cols or col < 0:
            return None
            # col = col - cols
        return self.grid[row][col]

    def __iter__(self):
        for row in self.grid:
            for cell in row:
                yield cell

    def combine_digits_2_numbers(self):
        for row in self.grid:
            actual_number = ""
            rel_cells = []
            row.append(Cell(row=1, col=1, value='.', cell_type=CellType.Empty))
            for i, cell in enumerate(row):
                if cell.value.isdigit():
                    actual_number += cell.value
                    rel_cells.append(cell)
                else:
                    for c in rel_cells:
                        c.value = int(actual_number)
                    actual_number = ""
                    rel_cells = []

    def get_neighbours(self, cell):
        offsets = [
            (-1, -1),
            ( 0, -1),
            (+1, -1),
            (-1,  0),
            ( 0,  0),
            (+1,  0),
            (-1, +1),
            ( 0, +1),
            (+1, +1),
        ]
        neighbours = {None}
        for o_r, o_c in offsets:
            neighbour = self.get_cell(cell.row + o_r, cell.col + o_c)
            neighbours.add(neighbour)
        neighbours.remove(None)
        return neighbours

    def get_x_neighbours(self, cell):
        offsets = [
            (-1, -1),
            (+1, -1),
            (-1, +1),
            (+1, +1),
        ]
        neighbours = {None}
        for o_r, o_c in offsets:
            neighbour = self.get_cell(cell.row + o_r, cell.col + o_c)
            neighbours.add(neighbour)
        neighbours.remove(None)
        return neighbours


def check_cell_rec(grid, cell, r_off, c_off, rest_search):
    if cell is None:
        return False
    if cell.value != rest_search[0]:
        return False
    if len(rest_search) == 1:
        return True

    n_row = cell.row + r_off
    n_col = cell.col + c_off
    n_cell = grid.get_cell(n_row, n_col)
    return check_cell_rec(grid, n_cell, r_off, c_off, rest_search[1:])


def func(grid, cell):
    neighbours = grid.get_neighbours(cell)
    for neighbour in neighbours:
        if neighbour.cell_type == CellType.Number:
            if type(neighbour.value) == str:
                print("gklan")
            part_number = neighbour.value
            for i in range(neighbour.col, -1, -1):
                if grid.grid[neighbour.row][i].cell_type == CellType.Number:
                    grid.grid[neighbour.row][i].cell_type == CellType.Empty
                    grid.grid[neighbour.row][i].value = '-'
                else:
                    break
            for i in range(neighbour.col, len(grid.grid[neighbour.row]), 1):
                if grid.grid[neighbour.row][i].cell_type == CellType.Number:
                    grid.grid[neighbour.row][i].cell_type == CellType.Empty
                    grid.grid[neighbour.row][i].value = '-'
                else:
                    break
            return part_number
    return None


def part1():
    grid = get_input()
    grid.combine_digits_2_numbers()
    rel_cells = [cell for cell in grid if cell.cell_type == CellType.Symbol]
    part_numbers = list()
    for cell in rel_cells:
        result = 1
        while result:
            result = func(grid, cell)
            part_numbers.append(result)

    print(f"The total of the relevant part numbers is {sum(part_numbers)}")


def part2():
    grid_og = get_input()
    grid_og.move_guard(limit=10000)
    print(grid_og)
    total = 0

    for i, cell in enumerate(grid_og):
        print(i)
        if cell.cell_type == CellType.Visited:
            grid = get_input()
            grid.grid[cell.row][cell.col].cell_type = CellType.Obstacle
            # print(grid)
            res = grid.move_guard(500)
            if not res:
                total += 1
    print(f"The total number of newly added obstacle is {total}")


if __name__ == '__main__':
    part1()
    # part2()
