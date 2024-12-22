import pathlib
import dataclasses


def get_input(demo=False) -> "Grid":
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    res = []

    for row, i in enumerate(inp):
        cell_row = []
        for col, j in enumerate(i):
            if j == ".":
                j = 100
            cell = Cell(row=row, col=col, value=int(j))
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

    def __str__(self):
        return "\n".join(["".join([cell.value for cell in row]) for row in self.grid])

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

    def get_cell_with_values(self, search_value) -> list[Cell]:
        res = list()
        for cell in self:
            if cell.value == search_value:
                res.append(cell)
        return res

    def get_t_neighbours(self, cell):
        offsets = [
            (0, -1),
            (-1, 0),
            (+1, 0),
            (0, +1),
        ]
        neighbours = {None}
        for o_r, o_c in offsets:
            neighbour = self.get_cell(cell.row + o_r, cell.col + o_c)
            neighbours.add(neighbour)
        neighbours.remove(None)
        return neighbours

    def get_neighbours(self, cell):
        offsets = [
            (-1, -1),
            (0, -1),
            (+1, -1),
            (-1, 0),
            (0, 0),
            (+1, 0),
            (-1, +1),
            (0, +1),
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


def rec2(grid, start_value, start_cells):
    trail_ends = list()
    for prev_cell in start_cells:
        if prev_cell is None:
            continue
        # print(prev_cell)

        neighbours = grid.get_t_neighbours(prev_cell)
        next_cells = [cell for cell in neighbours if cell.value - 1 == start_value]
        finished_cells = [cell for cell in next_cells if cell.value == 9]
        new_next_cells = [cell for cell in next_cells if cell not in finished_cells]
        # print(new_next_cells)
        for c in finished_cells:
            trail_ends.append(c)
        if new_next_cells:
            tmp = rec2(grid, start_value + 1, new_next_cells)
            trail_ends.extend(tmp)

    return trail_ends


def rec(grid, start_value, start_cells):
    trail_ends = set()
    for prev_cell in start_cells:
        if prev_cell is None:
            continue
        # print(prev_cell)

        neighbours = grid.get_t_neighbours(prev_cell)
        next_cells = [cell for cell in neighbours if cell.value - 1 == start_value]
        finished_cells = [cell for cell in next_cells if cell.value == 9]
        new_next_cells = [cell for cell in next_cells if cell not in finished_cells]
        # print(new_next_cells)
        for c in finished_cells:
            trail_ends.add(c)
        if new_next_cells:
            tmp = rec(grid, start_value + 1, new_next_cells)
            trail_ends |= tmp

    return trail_ends


def part1():
    grid = get_input()
    start_cells = grid.get_cell_with_values(0)
    counter = 0
    for start_cell in start_cells:
        neighbours = grid.get_t_neighbours(start_cell)
        trail_ends = rec(grid, start_cell.value + 1, [cell for cell in neighbours if cell.value == 1])
        counter += len(trail_ends)
        # print(len(trail_ends))
        # if len(trail_ends) == 3:
        #     print(1)
    print(f"The number of found hiking trails is: {counter}")


def part2():
    grid = get_input()
    start_cells = grid.get_cell_with_values(0)
    counter = 0
    for start_cell in start_cells:
        neighbours = grid.get_t_neighbours(start_cell)
        trail_ends = rec2(grid, start_cell.value + 1, [cell for cell in neighbours if cell.value == 1])
        counter += len(trail_ends)
        # print(len(trail_ends))
        # if len(trail_ends) == 24:
        #    print(1)
    print(f"The number of possible hiking trails is: {counter}")


if __name__ == '__main__':
    part1()
    part2()

