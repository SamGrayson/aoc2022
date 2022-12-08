import bisect


def count_calories(top_count=3):
    count_list = []
    current_count = 0

    with open("Day 1/input.txt") as calorie_input:
        for line in calorie_input:
            if line == "\n":
                bisect.insort(count_list, current_count)
                current_count = 0
            else:
                current_count += int(line.split("\n")[0])
        else:
            bisect.insort(count_list, current_count)

    list_end = len(count_list)

    return count_list[list_end - top_count : list_end]


max = count_calories()
print(sum(max))
