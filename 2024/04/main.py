import dataclasses
import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    res = []
    for row, i in enumerate(inp):
        cell_row = []
        for col, j in enumerate(i):
            cell = Cell(row=row, col=col, value=j)
            cell_row.append(cell)
        res.append(cell_row)
    return Grid(res)


@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    row: int
    col: int
    value: ""


class Grid:
    def __init__(self, grid):
        self.grid = grid

    def get_cell(self, row, col):
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


def rec1(grid, cell, rest_search, count):
    my_count = count
    if cell.value == rest_search[0]:
        if len(rest_search) == 1:
            return True
        for next_cell in grid.get_neighbours(cell):

            if rec1(grid, next_cell, rest_search[1:], my_count):
                my_count += 1
    else:
        return False

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


def part1():
    grid = get_input()
    total = 0
    search = "XMAS"
    for cell in grid:
        if cell.value == search[0]:
            for n_cell in grid.get_neighbours(cell):
                r_off = n_cell.row - cell.row
                c_off = n_cell.col - cell.col
                if check_cell_rec(grid, n_cell, r_off, c_off, search[1:]):
                    total += 1
    print(f"The total number of {search} occurrence is {total}")


def part2():
    grid = get_input()
    total = 0
    search = "MAS"
    for cell in grid:
        if cell.value == search[1]:

            axis = [
                [(cell.row-1, cell.col-1), (cell.row+1, cell.col+1)],
                [(cell.row-1, cell.col+1), (cell.row+1, cell.col-1)],
            ]
            res = False
            for ax in axis:
                res = False
                cell1 = grid.get_cell(*ax[0])
                cell2 = grid.get_cell(*ax[1])
                if cell1 and cell2:
                    for pos1, pos2 in [(0,2), (2,0)]:
                        if search[pos1] == cell1.value and search[pos2] == cell2.value:
                            res = True
                            break
                if not res:
                    break
            if res:
                total += 1

    print(f"The total number of X-{search} occurrence is {total}")


if __name__ == '__main__':
    part1()
    part2()
