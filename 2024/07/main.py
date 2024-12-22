import pathlib


def get_input(demo=True):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    res = []
    for i in inp:
        a = i.split(": ")
        sol = int(a[0])
        vals = a[1].strip().split(" ")
        res.append((sol, [int(v) for v in vals]))

    return res


from itertools import product


def func(operands):
    inp = get_input()
    valid_results = []
    total = 0
    for solution, dat in inp:
        variants = list(product(operands, repeat=len(dat) - 1))
        for var in variants:
            act_result = dat[0]
            for value, operand in zip(dat[1:], var):
                act_result = operand(act_result, value)
                if act_result > solution:
                    break
            if act_result == solution:
                valid_results.append((solution, dat))
                total += solution
                break

    print(f"The total number of valid data are: {len(valid_results)} with a total sum of {total}")


def part1():
    func([(lambda a, b: a * b), (lambda a, b: a + b)])


def part2():
    func([(lambda a, b: a * b), (lambda a, b: a + b), (lambda a, b: int(str(a) + str(b)))])


if __name__ == '__main__':
    part1()
    part2()
