import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n\n")
    rules_s = inp[0].strip().split("\n")
    jobs_s = inp[1].strip().split("\n")
    rules = []
    for r in rules_s:
        rule_s = r.split("|")
        rule = [int(r) for r in rule_s]
        rules.append(rule)

    jobs = []
    for r in jobs_s:
        job_s = r.split(",")
        job = [int(j) for j in job_s]
        jobs.append(job)
    return rules, jobs


def part1():
    rules, jobs = get_input()
    good_jobs = []
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
        if res:
            good_jobs.append(job)

    total = 0
    for job in good_jobs:
        i = (len(job) - 1) // 2
        total += job[i]

    print(f"The total number of good jobs are: {len(good_jobs)} with a total of the middle page {total}")


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
    part2()
