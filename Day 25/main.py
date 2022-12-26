num_key = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
decimal_key = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-"}


def convert(num):
    read = num[::-1]
    i = 0
    result = 0
    for n in read:
        if i == 0:
            power = 1
        else:
            power = 5**i
        result += num_key[n] * power
        i += 1

    return result


def convert_to_snafu(num):
    snafu = []
    while num > 0:
        num, mod = divmod(num, 5)
        snafu.insert(0, decimal_key[mod])
        if mod > 2:
            num += 1
    return "".join(snafu)


def part_1():

    values = []

    with open("Day 25/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            values.append(convert(line.strip()))

    return convert_to_snafu(sum(values))


res = part_1()
print(res)
