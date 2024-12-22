import pathlib
import re


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text()
    return inp


def calc_result(dat):
    res = 1
    for i in dat:
        res *= int(i)
    return res


def get_mul_sum(string):
    regex = r"mul\((\d{1,3}),(\d{1,3})\)"

    matches = list(re.finditer(regex, string, re.MULTILINE))
    result_len = len(list(matches))
    total = 0
    for match in matches:
        # founded_match = match.group()
        parts = match.groups()
        total += calc_result(parts)
    return result_len, total


def part1():
    data_str = get_input()

    result_len, total = get_mul_sum(data_str)

    print(f"The total number of operations are: {result_len} with a total of {total}")


def part2():
    dont = "don't()"
    do = "do()"

    data_str = get_input()
    data_str = " " + do + data_str
    # print(data_str.split(dont))
    total = 0
    tot_result = 0
    for i in data_str.split(dont):
        do_split = i.split(do)

        # print(do_split)
        for i in do_split[1:]:
            result_len, sum = get_mul_sum(i)
            total += sum
            tot_result += result_len

    print(f"The total number of operations are: {tot_result} with a total of {total}")

if __name__ == '__main__':
    part1()
    part2()
