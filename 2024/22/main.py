import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp_str = inp_file.read_text().split("\n")
    results = []
    for number in inp_str:
        results.append(int(number))
    return results


def is_possible(towels, actual_design: str):
    if actual_design == "":
        return True
    for towel in towels:
        if actual_design.startswith(towel):
            res = is_possible(towels, actual_design.removeprefix(towel))
            if res:
                return True
    return False


def mix_and_prune(sec, num):
    res1 = sec ^ num
    res2 = res1 % 16777216
    return res2


memo = {}


def calc_next_secret_number(secret1):
    secret2 = mix_and_prune(secret1, secret1 * 64)
    secret3 = mix_and_prune(secret2, int(secret2 / 32))
    secret4 = mix_and_prune(secret3, secret3 * 2048)
    return secret4


def part1():
    secret_numbers = get_input()
    sec2000 = []
    for sec in secret_numbers:
        new_sec = sec
        for _ in range(2000):
            new_sec = calc_next_secret_number(new_sec)
        sec2000.append(new_sec)
    print(f"The total number of all the 2000th secret numbers is: {sum(sec2000)}")


def part2():
    secret_numbers = get_input()
    all_data = []
    for sec in secret_numbers:
        new_sec = sec
        actual_secrets = [new_sec]
        for _ in range(2000):
            new_sec = calc_next_secret_number(new_sec)
            actual_secrets.append(new_sec)
        # all_data[sec] = actual_secrets
        prices = [secrete % 10 for secrete in actual_secrets]
        changes = [f'{p - prices[i]:+d}' for i, p in enumerate(prices[1:])]
        all_data.append({"p": prices, "c": ", ".join(changes)})

    combinations = [[a, b, c, d, e] for e in range(10) for d in range(10) for c in range(10) for b in range(10) for a in range(10)]
    all_changes = list()
    for combo in combinations:
        changes = [f'{p - combo[i]:+d}' for i, p in enumerate(combo[1:])]
        changes_str = ", ".join(changes)
        if changes_str in all_changes:
            all_changes.append(None)
        else:
            all_changes.append(changes_str)

    price_sums = []
    print("425")
    for idx, master_change in enumerate(all_changes):
        if master_change is None:
            continue
        # master_change = [int(c) for c in master_change.split(", ")]

        print(idx)
        # master_change = [-1, -1, 0, 2]
        # master_change = [-2, 1, -1, 3]
        price_sum = 0
        for data in all_data:
            changes = data["c"]
            found_price_idx = 0
            res = changes.find(master_change)
            if res > 0:
                found_price_idx = res // 4 + 4
            # for i in range(len(changes)-3):
            #     c4 = [changes[i+j] for j in range(4)]
            #     if c4 == master_change:
            #         found_price_idx = i + 4
            #         break
            if found_price_idx > 0:
                price = data["p"][found_price_idx]
                price_sum += price
        price_sums.append(price_sum)

    change = all_changes[price_sums.index(max(price_sums))]
    # for comb in combinations:
    # for dat in all_data:
    print(f"The best number of bananas is: {max(price_sums)} with a the combo {change}")


if __name__ == '__main__':
    # part1()
    part2()
