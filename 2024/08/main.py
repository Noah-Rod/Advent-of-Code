import dataclasses
import pathlib


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
            cell = Cell(row=row, col=col, value=j, anti_node=False)
            cell_row.append(cell)
        res.append(cell_row)
    return Grid(res)


@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    row: int
    col: int
    value: ""
    anti_node: bool = False


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

    def __iter__(self) -> Cell:
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


def part1():
    grid = get_input()
    antennas = {}
    for cell in grid:
        if cell.value in antennas.keys():
            antennas[cell.value].append(cell)
        else:
            antennas[cell.value] = [cell]

    for antenna, cells in antennas.items():
        # print(antenna)
        if antenna == '.' or antenna == '#':
            continue
        for og_cell in cells:
            for cell in cells:
                if cell == og_cell:
                    continue
                an_1 = grid.get_cell(og_cell.row + (og_cell.row - cell.row), og_cell.col + (og_cell.col - cell.col))
                an_2 = grid.get_cell(cell.row - (og_cell.row - cell.row), cell.col - (og_cell.col - cell.col))
                if an_1 and an_1 != cell and an_1 != og_cell:
                    an_1.anti_node = True
                if an_2 and an_2 != cell and an_2 != og_cell:
                    an_2.anti_node = True

    total = 0
    for cell in grid:
        if cell.anti_node:
            total += 1
    print(f"The total number of anti nodes are: {total}")


def part2():
    grid = get_input()
    antennas = {}
    for cell in grid:
        if cell.value in antennas.keys():
            antennas[cell.value].append(cell)
        else:
            antennas[cell.value] = [cell]

    for antenna, cells in antennas.items():
        print(antenna)
        if antenna == '.' or antenna == '#':
            continue
        for og_cell in cells:
            for cell in cells:
                if cell == og_cell:
                    continue
                offset_r, offset_c = (og_cell.row - cell.row), (og_cell.col - cell.col)
                anti_node = 1
                factor = 0
                while anti_node is not None:
                    anti_node = grid.get_cell(og_cell.row + offset_r * factor, og_cell.col + offset_c * factor)
                    if anti_node:
                        anti_node.anti_node = True
                    factor += 1
                anti_node = 1
                factor = 0
                while anti_node is not None:
                    anti_node = grid.get_cell(og_cell.row - offset_r * factor, og_cell.col - offset_c * factor)
                    if anti_node:
                        anti_node.anti_node = True
                    factor += 1


    total = 0
    for cell in grid:
        if cell.anti_node:
            total += 1
    print(f"The total number of anti nodes are: {total}")


if __name__ == '__main__':
    part1()
    part2()
