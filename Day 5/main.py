"""
[N]             [R]             [C]
[T] [J]         [S] [J]         [N]
[B] [Z]     [H] [M] [Z]         [D]
[S] [P]     [G] [L] [H] [Z]     [T]
[Q] [D]     [F] [D] [V] [L] [S] [M]
[H] [F] [V] [J] [C] [W] [P] [W] [L]
[G] [S] [H] [Z] [Z] [T] [F] [V] [H]
[R] [H] [Z] [M] [T] [M] [T] [Q] [W]
 1   2   3   4   5   6   7   8   9 
"""

# Sample
# crates = {
#     1: ['N', 'Z'],
#     2: ['D', 'C', 'M'],
#     3: ['P']
# }


crates = {
    1: ["N", "T", "B", "S", "Q", "H", "G", "R"],
    2: ["J", "Z", "P", "D", "F", "S", "H"],
    3: ["V", "H", "Z"],
    4: ["H", "G", "F", "J", "Z", "M"],
    5: ["R", "S", "M", "L", "D", "C", "Z", "T"],
    6: ["J", "Z", "H", "V", "W", "T", "M"],
    7: ["Z", "L", "P", "F", "T"],
    8: ["S", "W", "V", "Q"],
    9: ["C", "N", "D", "T", "M", "L", "H", "W"],
}

"""
EX: move 3 from 9 to 7
"""


def part_1():

    top = []

    with open("Day 5/input.txt") as data:
        # EX : A X
        for line in data:
            split = line.split(" ")
            # Amount to move
            amount = int(split[1])
            # From A
            a = int(split[3])
            # To B
            b = int(split[5].replace("\n", ""))

            # Get the creates & their moving order
            moving = crates[a][0:amount]
            moving.reverse()

            # Remove the crates since they're moving
            del crates[a][0:amount]

            # Add the crates to the bottom of the new moving list
            moving.extend(crates[b])

            # That's the new value for the stack
            crates[b] = moving

    # Get the top of each stack into an array
    for item in crates.items():
        top.append(item[1][0])

    # Return the top of each stack
    return "".join(top)


"""Dont Reverse"""


def part_2():

    top = []

    with open("Day 5/input.txt") as data:
        # EX : A X
        for line in data:
            split = line.split(" ")
            # Amount to move
            amount = int(split[1])
            # From A
            a = int(split[3])
            # To B
            b = int(split[5].replace("\n", ""))

            # Get the creates & their moving order
            moving = crates[a][0:amount]

            # Remove the crates since they're moving
            del crates[a][0:amount]

            # Add the crates to the bottom of the new moving list
            moving.extend(crates[b])

            # That's the new value for the stack
            crates[b] = moving

    # Get the top of each stack into an array
    for item in crates.items():
        top.append(item[1][0])

    # Return the top of each stack
    return "".join(top)


res = part_2()
print(res)
