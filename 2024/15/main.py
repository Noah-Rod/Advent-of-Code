import pathlib
import re
import dataclasses


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp_str = inp_file.read_text().split("\n\n")
    field_s = inp_str[0]
    rows = []
    start_pos = (0,0)
    for r, row_s in enumerate(field_s.split("\n")):
        row = []
        for c, cell_s in enumerate(row_s):
            cell = Cell(row=r, col=c)
            if cell_s == '#':
                cell.border = True
            elif cell_s == 'O':
                cell.box = True
            elif cell_s == '@':
                start_pos = cell
            row.append(cell)
        rows.append(row)
    movements_s = inp_str[1].replace("\n", "")

    movements = list()
    for move in movements_s:
        if move == ">":
            move_xy = (1, 0)
        elif move == "<":
            move_xy = (-1, 0)
        elif move == "^":
            move_xy = (0, -1)
        if move == "v":
            move_xy = (0, 1)
        movements.append(move_xy)
    return start_pos, Grid(rows), movements


def get_input2(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp_str = inp_file.read_text().split("\n\n")
    field_s = inp_str[0]
    rows = []
    start_pos = None
    for r, row_s in enumerate(field_s.split("\n")):
        row = []
        for c, cell_s in enumerate(row_s):
            cell1 = Cell(row=r, col=c*2)
            cell2 = Cell(row=r, col=c*2 + 1)
            if cell_s == '#':
                cell1.border = True
                cell2.border = True
            elif cell_s == 'O':
                cell1.box_r = True
                cell2.box_l = True
            elif cell_s == '@':
                start_pos = cell1
            row.append(cell1)
            row.append(cell2)
        rows.append(row)
    movements_s = inp_str[1].replace("\n", "")

    movements = list()
    for move in movements_s:
        if move == ">":
            move_xy = (1, 0)
        elif move == "<":
            move_xy = (-1, 0)
        elif move == "^":
            move_xy = (0, -1)
        if move == "v":
            move_xy = (0, 1)
        movements.append(move_xy)
    return start_pos, Grid(rows), movements


@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    row: int
    col: int
    # value: str
    border: bool = False
    box: bool = False
    box_r: bool = False
    box_l: bool = False

    def _order_value(self):
        return self.row * 1_000_000 + self.col


class Grid:
    def __init__(self, grid):
        self.grid: list[list[Cell]] = grid

    def __str__(self):
        return "\n".join(["".join([str(cell.value) for cell in row]) for row in self.grid])

    def print(self, robot):
        for row in self.grid:
            row_s = ""
            for cell in row:
                if cell.border:
                    row_s += "#"
                elif cell.box:
                    row_s += "O"
                elif cell.box_r:
                    row_s += "]"
                elif cell.box_l:
                    row_s += "["
                elif cell == robot:
                    row_s += "@"
                else:
                    row_s += "."
            print(row_s)
        # return "\n".join(["".join([str(cell.value) for cell in row]) for row in self.grid])

    def add_border_with_neg(self, value):
        for row in range(len(self.grid)):
            self.grid[row].insert(0, Cell(row=row, col=-1, value=value))
            self.grid[row].append(Cell(row=row, col=len(self.grid[row])-1, value=value))
        self.grid.insert(0, [Cell(row=-1, col=i, value=value) for i in range(-1, len(self.grid[0])-1)])
        self.grid.append([Cell(row=len(self.grid), col=i, value=value) for i in range(-1, len(self.grid[-1])-1)])

    def add_border_and_recount(self, value):
        self.add_border_with_neg(value)

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.grid[row][col].row = row
                self.grid[row][col].col = col

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

    def _get_units(self, cell, unit: set[Cell]) -> set[Cell]:
        neighbours = self.get_t_neighbours(cell)
        rel_n = {n for n in neighbours if n.value == cell.value and n not in unit}
        if len(rel_n) <= 0:
            return unit
        new_unit = unit.union(rel_n)
        for n in rel_n:
            new_unit = new_unit.union(self._get_units(n, new_unit))
        return new_unit

    def get_units(self):
        remaining_cells = set(self)
        units = list()
        for cell in self:
            if cell in remaining_cells:
                act_unit = self._get_units(cell, {cell})
                remaining_cells = remaining_cells.difference(act_unit)
                units.append(act_unit)
            if len(remaining_cells) <= 0:
                break
        return units

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

    def get_next_cc_neighbour_value(self, cell, value):
        offsets = [
            (-1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]
        for o_r, o_c in offsets:
            neighbour = self.get_cell(cell.row + o_r, cell.col + o_c)
            if neighbour.value == value:
                return neighbour
        return None

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


def part1():
    robot_cell, grid, movements = get_input()
    for move in movements:
        grid.print(robot_cell)
        print(move)
        cell = grid.get_cell(robot_cell.row + move[1], robot_cell.col + move[0])
        if cell.border:
            pass
        elif cell.box_r or cell.box_l:
            new_cells = [cell]
            if cell.box_l:
                new_cells.append(grid.get_cell(cell.row, cell.col + 1))
            else:
                new_cells.append(grid.get_cell(cell.row, cell.col - 1))
            while True:
                for new_cell in new_cells:
                    if new_cell.box_l:
                        new_cell = grid.get_cell(new_cell.row + move[1], new_cell.col + move[0])
                    new_cell
                    if new_cell.border:
                        break
                    elif not new_cell.box_r and not new_cell.box_l:
                        cell.box = False
                        robot_cell = cell
                        new_cell.box = True
                        break

        else:
            robot_cell = cell

    total = 0
    for cell in grid:
        if cell.box_l:
            total += cell.row * 100 + cell.col

    grid.print(robot_cell)
    print(f"The total number of the GPS is: {total}")


def part2():
    robot_cell, grid, movements = get_input2()
    for move in movements:
        # grid.print(robot_cell)
        # print(move)
        cell = grid.get_cell(robot_cell.row + move[1], robot_cell.col + move[0])
        if cell.border:
            pass
        elif cell.box:
            new_cell = cell
            while True:
                new_cell = grid.get_cell(new_cell.row + move[1], new_cell.col + move[0])
                if new_cell.border:
                    break
                elif not new_cell.box:
                    cell.box = False
                    robot_cell = cell
                    new_cell.box = True
                    break

        else:
            robot_cell = cell

    total = 0
    for cell in grid:
        if cell.box:
            total += cell.row * 100 + cell.col

    grid.print(robot_cell)
    print(f"The total number of the GPS is: {total}")


if __name__ == '__main__':
    part1()
    # part2()