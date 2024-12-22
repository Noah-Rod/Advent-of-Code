import pathlib
import re


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    return inp


def get_number(string):
    regex = r"\d"

    matches = list(re.finditer(regex, string, re.MULTILINE))
    number = matches[0].group() + matches[-1].group()

    # for match in matches:
    #     founded_match = match.group()

    return int(number)


def part1():
    data = get_input()
    total = 0
    for dat in data:
        regex = r"\d"

        matches = list(re.finditer(regex, dat, re.MULTILINE))
        number_str = matches[0].group() + matches[-1].group()

        number = int(number_str)
        total += number

    print(f"The total of the numbers is {total}")


def part2():
    data = get_input()
    lp = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}
    regex = r"(?=(\d|" + "|".join(lp.keys()) + "))"
    total = 0
    for dat in data:

        matches = list(re.findall(regex, dat))
        number_str = matches[0] + matches[-1]
        for k, v in lp.items():
            number_str = number_str.replace(k, str(v))
        number = int(number_str)
        total += number

    print(f"The total of the numbers is {total}")


if __name__ == '__main__':
    # part1()
    part2()
