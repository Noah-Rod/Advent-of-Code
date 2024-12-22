import pathlib
import re
import dataclasses


@dataclasses.dataclass
class XY:
    x: int
    y: int


@dataclasses.dataclass
class Robot:
    pos: XY
    vel: XY


def get_input(demo=False) -> list[Robot]:
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    robots_s = inp_file.read_text().split("\n")
    robots = []
    for robot_s in robots_s:
        r = r"p=(-?\d+)\,(-?\d+).*v=(-?\d+)\,(-?\d+).*"
        dat = re.findall(r, robot_s)[0]
        robot = Robot(pos=XY(x=int(dat[0]), y=int(dat[1])), vel=XY(x=int(dat[2]), y=int(dat[3])))
        robots.append(robot)
    return robots


def print_r(robots: list[Robot], pp=True):
    xx = max(robots, key=lambda r: r.pos.x).pos.x + 1
    yy = max(robots, key=lambda r: r.pos.y).pos.y + 1
    plot = []
    robot_dict = {}
    robot_dict_y = {}
    for robot in robots:
        robot_dict[(robot.pos.x, robot.pos.y)] = robot
    # for robot in robots:
    #     robot_dict_y[robot.pos.y] = robot

    for y in range(yy):
        sub_plot = []
        for x in range(xx):
            count = 0
            if (x, y) in robot_dict.keys():
                count += 1
            if count == 0:
                count = '.'
            sub_plot.append(count)
            if pp:
                print(count, end="")
        pre_t = '.'
        one_count = 0
        for t in sub_plot:
            if pre_t == t and t != '.':
                one_count += 1
                if one_count >= 10:
                    if not pp:
                        print_r(robots, True)
                        return
            else:
                one_count = 0
            pre_t = t

        if pp:
            print("")
        # plot.append(sub_plot)

def part1():
    robots = get_input()
    grid_x = 101
    grid_y = 103

    # grid_x = 11
    # grid_y = 7

    print_r(robots, False)

    print_r(robots)
    for count in range(10_000):
        print(count)
        for robot in robots:
            robot.pos.x = (robot.pos.x + robot.vel.x) % grid_x
            robot.pos.y = (robot.pos.y + robot.vel.y) % grid_y
        # if 9000 >= count > 8000:
        print_r(robots, False)

    print_r(robots)

    quadrants = 4 * [0]
    for robot in robots:
        if robot.pos.x > grid_x // 2:
            if robot.pos.y > grid_y // 2:
                quadrants[0] += 1
            if robot.pos.y < grid_y // 2:
                quadrants[1] += 1
        if robot.pos.x < grid_x // 2:
            if robot.pos.y > grid_y // 2:
                quadrants[2] += 1
            if robot.pos.y < grid_y // 2:
                quadrants[3] += 1
    res = 1
    for q in quadrants:
        res *= q
    print(f"The total safety factor is: {res}")


def part2():
    rules, jobs = get_input()
    bad_jobs = []
    for job in jobs:
        def _check_rules():
            for rule in rules:
                indexes = []
                try:
                    for page in rule:
                        index = job.index(page)
                        indexes.append(index)
                    t = indexes.copy()
                    t.sort()
                    if t != indexes:
                        return False
                except ValueError:
                    pass
            return True

        res = _check_rules()
        if not res:
            bad_jobs.append(job)

    def flip(job):
        while True:
            def _check_rules(_job):
                for rule in rules:
                    indexes = []
                    try:
                        for page in rule:
                            index = _job.index(page)
                            indexes.append(index)
                        t = indexes.copy()
                        t.sort()
                        if t != indexes:
                            for ii, i in enumerate(indexes):
                                _job[i], _job[t[ii]] = _job[t[ii]], _job[i]
                                return False, _job
                    except ValueError:
                        pass
                return True, _job

            res, job = _check_rules(job)
            if res:
                return job

    fixed_jobs = []
    for job in bad_jobs:
        res = flip(job)
        fixed_jobs.append(res)

    total = 0
    for job in bad_jobs:
        i = (len(job) - 1) // 2
        total += job[i]

    print(f"The total number of bad good jobs are: {len(bad_jobs)} with a total of the middle page {total}")


if __name__ == '__main__':
    part1()
    # part2()