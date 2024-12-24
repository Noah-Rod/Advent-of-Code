import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp_str = inp_file.read_text().split("\n")
    results = []
    for computers_s in inp_str:
        results.append(computers_s.split("-"))
    return results


def part1():
    connections = get_input()
    computers = set()
    for connection in connections:
        computers.add(connection[0])
        computers.add(connection[1])
    comp_dict = dict()
    for computer in computers:
        comp_dict[computer] = []

    for connection in connections:
        comp_dict[connection[0]].append(connection[1])
        comp_dict[connection[1]].append(connection[0])

    three_comps = set()

    for computer in comp_dict.keys():
        connected_computers = comp_dict[computer]

        for comp in connected_computers:
            con_connected_computers = comp_dict[comp]
            for comp3 in con_connected_computers:
                if computer in comp_dict[comp3]:
                    three_comps.add(frozenset([computer, comp, comp3]))

    t_sets = set()
    for comps in three_comps:
        if any([str(c).startswith('t') for c in comps]):
            t_sets.add(comps)
    print(f"The total number of 3 computer connections with a t computer is: {len(t_sets)}")


def part2():
    connections = get_input()
    computers = set()
    for connection in connections:
        computers.add(connection[0])
        computers.add(connection[1])
    comp_dict = dict()
    for computer in computers:
        comp_dict[computer] = []

    for connection in connections:
        comp_dict[connection[0]].append(connection[1])
        comp_dict[connection[1]].append(connection[0])

    def fi(comps, rem):
        if rem == 0:
            return []
        for c in comps:
            new_comps = filter(lambda x: x != c and (x in comp_dict[c]), comps)
            ret = fi(new_comps, rem - 1)
            if ret != -1:
                ret.append(c)
                return ret
        return -1

    found_comb = -1
    for i in range(1, 100):
        ret = fi(list(computers), i)
        if ret == -1:
            break
        found_comb = ret

    found_comb = list(found_comb)
    found_comb.sort()
    res = ",".join(found_comb)

    print(f"The number_of computers is: {len(found_comb)} with the password being: {res}")


if __name__ == '__main__':
    part1()
    part2()
