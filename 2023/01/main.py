import pathlib
import re


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    game_data = []
    for i in inp:
        data_r = i.strip().split(":")
        game = data_r[0]
        game_id = int(game.split(" ")[1].strip())
        data_s = data_r[1]
        sets_s = data_s.strip().split(";")
        sets = []
        for s in sets_s:
            turns_s = s.strip().split(",")
            turns = {}
            for t in turns_s:
                turn = t.strip().split(" ")
                number = turn[0]
                colour = turn[1]
                turns[colour] = int(number)
            sets.append(turns)
        game_data.append((game_id, sets))
    return game_data


def check_draw(draw, limits):
    for colour, max_number in limits.items():
        if draw.get(colour, 0) > max_number:
            return False
    return True

def part1():
    data = get_input()
    limits = {"red": 12, "green": 13, "blue": 14}
    total = 0
    for game, dat in data:

        print(game, dat)
        for draw in dat:
            if not check_draw(draw, limits):
                break
        else:
            print(game, dat)
            total += game
    print(f"The total sum of the correct Game IDs is {total}")

def part2():
    data = get_input()
    start_values = {"red": 0, "green": 0, "blue": 0}
    total = 0
    for game, dat in data:

        print(game, dat)
        start_values = {"red": 0, "green": 0, "blue": 0}
        for draw in dat:
            for colour, number in draw.items():
                if start_values[colour] < number:
                    start_values[colour] = number
        else:
            print(game, dat)
            res = 1
            for value in start_values.values():
                res *= value
            total += res
    print(f"The total sum of the correct Game IDs is {total}")
    print(f"The total of the numbers is {total}")


if __name__ == '__main__':
    part1()
    part2()
