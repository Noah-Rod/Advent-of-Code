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
            cell = Cell(row=row, col=col, value=j)
            cell_row.append(cell)
        res.append(cell_row)
    return Grid(res)


@dataclasses.dataclass(unsafe_hash=True)
class Cell:
    row: int
    col: int
    value: str

    def _order_value(self):
        return self.row * 1_000_000 + self.col

class Grid:
    def __init__(self, grid):
        self.grid: list[list[Cell]] = grid

    def __str__(self):
        return "\n".join(["".join([str(cell.value) for cell in row]) for row in self.grid])

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
    grid = get_input()
    units = grid.get_units()
    total_price = 0
    for unit in units:
        perimeter = 0
        area = len(unit)
        for cell in unit:
            neighbours = grid.get_t_neighbours(cell)
            perimeter += (4 - len(neighbours))
            perimeter_cells = [n for n in neighbours if n.value != cell.value]
            perimeter += len(perimeter_cells)
        price = area * perimeter
        total_price += price
        # print(f"{cell.value}: {price} = {area=} * {perimeter=}")
    print(f"The number of units is: {len(units)} with a total price of {total_price}")


def part2():
    grid = get_input()
    grid.add_border_and_recount('*')
    units = grid.get_units()
    print("removed unit with value", units.pop(0).pop().value)
    total_price = 0
    for unit in units:
        area = len(unit)
        half_grid = []
        for main_cell in unit:
            neighbours = grid.get_t_neighbours(main_cell)
            perimeter_cells = [n for n in neighbours if n.value != main_cell.value]
            for p_cell in perimeter_cells:
                if main_cell.col == p_cell.col:
                    half_grid.append(Cell(row=(main_cell.row*3 + p_cell.row)/4, col=main_cell.col, value="-"))
                if main_cell.row == p_cell.row:
                    half_grid.append(Cell(row=main_cell.row, col=(main_cell.col*3 + p_cell.col)/4, value="|"))

        # print(half_grid)
        perimeter_dict_r = dict()
        perimeter_dict_c = dict()
        perimeter_dict = {'-': dict(), '|': dict()}
        for cell in half_grid:
            if cell.value == '-':
                if cell.row in perimeter_dict[cell.value].keys():
                    perimeter_dict[cell.value][cell.row].append(cell.col)
                else:
                    perimeter_dict[cell.value][cell.row] = [cell.col]

            if cell.value == '|':
                if cell.col in perimeter_dict[cell.value].keys():
                    perimeter_dict[cell.value][cell.col].append(cell.row)
                else:
                    perimeter_dict[cell.value][cell.col] = [cell.row]
        side_counter = 0
        for d in perimeter_dict.values():
            for rc in d.values():
                rel = rc.copy()
                rel.sort()
                side_counter += 1
                actual_element = min(rc)
                has_break = False
                for control_index in range(min(rc), max(rc) + 1):
                    if control_index not in rel:
                        if has_break:
                            continue
                        else:
                            has_break = True
                            side_counter += 1
                    else:
                        has_break = False

        # unit_l = list(unit)
        # unit_l.sort(key=Cell._order_value)
        # start = unit_l[0]
        # next_cell = None
        # prev_cell = start
        # perimeter += 1
        # h_or_v = True
        # while start != next_cell:
        #     next_cell = grid.get_next_cc_neighbour_value(prev_cell, start.value)
        #     if h_or_v and start.row != next_cell.row:
        #         perimeter += 1
        #         h_or_v = not h_or_v
        #
        #     if not h_or_v and start.col != next_cell.col:
        #         perimeter += 1
        #         h_or_v = not h_or_v
        #     prev_cell = next_cell
        price = area * side_counter
        total_price += price
        print(f"{main_cell.value}: {price} = {area=} * {side_counter=}")
    print(f"The number of units is: {len(units)} with a total price of {total_price}")


if __name__ == '__main__':
    part1()
    part2()

