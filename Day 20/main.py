# Keep track of the amount of nums so we can add them to the value to track duplicates
found_nums = {}


def part_1():
    num_list_start = []
    num_list = []
    with open("Day 20/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            found_nums[int(line)] = found_nums.get(int(line), 0) + 1
            num_list_start.append(f"{found_nums[int(line)]}_{int(line)}")

    # Array to modify
    num_list = num_list_start.copy()

    while num_list_start:
        # Num to move
        num = num_list_start.pop(0)
        num_clean = int(num.split("_")[1])

        if num_clean == 0:
            continue

        # Index
        index = num_list.index(num)

        # Also pop the #
        num_to_move = num_list.pop(index)

        # Calculate index fron num.
        new_idx = index + num_clean
        new_idx %= len(num_list)

        # Move the number first
        num_list.insert(new_idx, num_to_move)

    # zero index:
    z_index = num_list.index("1_0")

    # after 0 list
    # check_list = num_list[z_index:] + num_list[:z_index]

    # 1000th + 2000th + 3000th after 0
    one_t = int(num_list[(z_index + 1000) % len(num_list)].split("_")[1])
    two_t = int(num_list[(z_index + 2000) % len(num_list)].split("_")[1])
    three_t = int(num_list[(z_index + 3000) % len(num_list)].split("_")[1])

    print(one_t, two_t, three_t)

    return one_t + two_t + three_t


res = part_1()

print(res)
