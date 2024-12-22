import pathlib


def get_input(demo=False):
    if demo:
        inp_file = pathlib.Path(__file__).parent / "demo.txt"
    else:
        inp_file = pathlib.Path(__file__).parent / "input.txt"
    inp = inp_file.read_text().split("\n")
    res = []
    for i in inp:
        a = i.strip()
        res.append(a)
    return res


def uncompress():
    compressed_data = get_input()
    print(len(compressed_data[0]), compressed_data[0])
    orig_data = []
    orig_data_ids = []
    for d_str in compressed_data:
        res = []
        for i, num_s in enumerate(d_str):
            num = int(num_s)
            if i % 2 == 0:
                res.extend(num * [i // 2])
                orig_data_ids.extend(2 * [i // 2])
            else:
                res.extend(num * ['.'])

        orig_data.append(res)

    print(len(orig_data[0]))
    return orig_data


def part1():
    orig_data = uncompress()

    new_crc = 0

    for d_str in orig_data:
        data = list(d_str)
        data_r = list(d_str)
        # while '.' in data_r:
        #     data_r.remove('.')

        data_r.reverse()
        max_idx = len(data)
        new_data = []
        for idx, value in enumerate(data):
            if idx >= max_idx:
                break
            if value == '.':
                n = '.'
                while n == '.':
                    n = data_r.pop(0)
                    max_idx -= 1
                new_data.append(n)
            else:
                new_data.append(value)
        # print("calc_crc")
        # new_data = data[:max_idx-1]
        # print(new_data)
        # return new_data

        for idx, val in enumerate(new_data):
            new_crc += val * idx
        # print(new_crc)
    # result_len, total = get_mul_sum(data_str)
    #
    print(f"The new calculated crc is: {new_crc} with a length of {len(new_data)}")


def part2():
    orig_data = uncompress()
    # print(orig_data)
    new_crc = 0
    for dat in orig_data:
        new_data = dat.copy()

        for file_id in range(new_data[-1], 0, -1):
            # print(file_id)
            dat_r = list(new_data)
            dat_r.reverse()
            # get last block
            moving_block_size = dat_r.count(file_id)
            start_moving_block = new_data.index(file_id)
            # print("origin_value: ", new_data)

            counter = 0
            for idx, v in enumerate(new_data):
                if v == '.':
                    counter += 1
                else:
                    counter = 0
                if idx > start_moving_block:
                    break
                if counter >= moving_block_size:
                    for sub_idx in range(moving_block_size):
                        new_data[(idx - counter) + sub_idx + 1] = file_id
                    # new_data = new_data[:-moving_block_size]
                    # print("moved_value:  ", new_data)
                    for sub_idx in range(moving_block_size):
                        new_data[start_moving_block + sub_idx] = '.'
                    # print("removed_value:", new_data)

                    break

        # print(new_data)
        for idx, val in enumerate(new_data):
            if val != '.':
                new_crc += int(val) * idx
        print(new_crc)
    print(f"The new calculated crc is: {new_crc} with a length of {len(new_data)}")


if __name__ == '__main__':
    part1()
    part2()
