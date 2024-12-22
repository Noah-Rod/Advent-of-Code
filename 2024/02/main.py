import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    reports = []
    for line in inp:
        levels = line.split()
        reports.append([int(lev) for lev in levels])
    return reports


def rec_checker(actual, rest, pos_neg):
    if len(rest) == 0:
        return True
    if pos_neg:
        if (rest[0]+3) >= actual > rest[0]:
            return rec_checker(rest[0], rest[1:], pos_neg)
        else:
            return False
    else:
        if (rest[0]-3) <= actual < rest[0]:
            return rec_checker(rest[0], rest[1:], pos_neg)
        else:
            return False

def part1():
    reports = get_input()
    valid_reports = []
    for report in reports:
        pos = rec_checker(report[0], report[1:], True)
        neg = rec_checker(report[0], report[1:], False)
        if pos or neg:
            valid_reports.append(report)

    print(f"The number of valid reports is: {len(valid_reports)} of {len(reports)}")


def part2():
    reports = get_input()
    valid_reports = []
    for report in reports:
        for i in range(len(report)+1):
            new_report = report.copy()
            if i < len(report):
                new_report.pop(i)
            pos = rec_checker(new_report[0], new_report[1:], True)
            neg = rec_checker(new_report[0], new_report[1:], False)
            if pos or neg:
                valid_reports.append(report)
                # print(report)
                break

    print(f"The number of valid reports (with Problem Dampener) is: {len(valid_reports)} of {len(reports)}")

if __name__ == '__main__':
    part1()
    part2()
