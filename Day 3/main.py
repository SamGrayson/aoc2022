"""
Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.
"""
import string

# Get the priroity map generated for each character
chars = [*string.ascii_lowercase, *string.ascii_uppercase]

priority_map = {}

l_count = 1
for c in chars:
    priority_map[c] = l_count
    l_count += 1


def part_1():
    # Generate the output
    total = 0
    with open("Day 3/input.txt") as data:
        # EX : A X
        #
        for line in data:
            clean = line.replace("\n", "")
            p1 = clean[: len(clean) // 2]
            p2 = clean[len(clean) // 2 :]

            inter = set(p1).intersection(p2)

            res = priority_map[list(inter)[0]] if len(inter) > 0 else 0

            total = total + res

    return total


"""
3 rows = a group
"""


def part_2():
    chunk = []
    total = 0

    def getIntersectionList(arr):
        return list(set.intersection(*map(set, arr)))

    with open("Day 3/input.txt") as data:
        # Chunk the lines into 3, then do the logic
        for line in data:
            if len(chunk) == 3:
                inter = getIntersectionList(chunk)
                total = total + priority_map[inter[0]] if len(inter) > 0 else 0
                chunk = []
            chunk.append(line.replace("\n", ""))
        else:
            # Go ahead and calculate the left overs (may be 1 - 3)
            if len(chunk) > 0:
                inter = getIntersectionList(chunk)
                total = total + priority_map[inter[0]] if len(inter) > 0 else 0

    return total


res = part_2()
print(res)
