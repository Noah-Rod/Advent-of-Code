import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp_str = inp_file.read_text().split("\n\n")
    towels_s = inp_str[0]
    towels = []
    for towel_s in towels_s.split(", "):
        towels.append(towel_s)

    designs_s = inp_str[1]
    designs = []
    for design_s in designs_s.split("\n"):
        designs.append(design_s)

    return towels, designs


def is_possible(towels, actual_design: str):
    if actual_design == "":
        return True
    for towel in towels:
        if actual_design.startswith(towel):
            res = is_possible(towels, actual_design.removeprefix(towel))
            if res:
                return True
    return False


def part1():
    towels, designs = get_input()
    possible = []
    for d in designs:
        res = is_possible(towels, d)
        if res:
            possible.append(d)

    print(f"The total number of possible design is: {len(possible)}")

memo = {}

def find(towels, actual_design: str):
    if actual_design == "":
        return 1
    counter = 0
    if actual_design in memo.keys():
        return memo[actual_design]
    for towel in towels:
        if actual_design.startswith(towel) and actual_design not in memo.keys():
            res = find(towels, actual_design.removeprefix(towel))
            counter += res

    memo[actual_design] = counter
    return counter


def part2():
    towels, designs = get_input()
    possible = []
    combinations = []
    for i, d in enumerate(designs):
        print((i/len(designs))*100)
        res = find(towels, d)
        if res > 0:
            possible.append(d)
            combinations.append(res)

    print(f"The total number of possible design is: {len(possible)} with a total combinations {sum(combinations)}")


if __name__ == '__main__':
    part1()
    part2()
