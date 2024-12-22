import pathlib

def get_input():
    # inp_file = pathlib.Path(__file__).parent / "demo.txt"
    inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    li_l = []
    li_r = []
    for line in inp:
        l, r = line.split()
        li_l.append(int(l))
        li_r.append(int(r))
    return li_l, li_r

def part1():
    li_l, li_r = get_input()
    li_r.sort()
    li_l.sort()
    distance = []
    for r, l in zip(li_r, li_l):
        distance.append(abs(r - l))

    print(f"The sum of the distance is: {sum(distance)}")


def part2():
    li_l, li_r = get_input()
    di_r = {}
    for el in li_r:
        if el in di_r.keys():
            di_r[el] += 1
        else:
            di_r[el] = 1
    sim_score = 0
    for el in li_l:
        if el in di_r.keys():
            sim_score += el * di_r[el]

    print(f"The sim score of the distances is: {sim_score}")


if __name__ == '__main__':
    part1()
    part2()
