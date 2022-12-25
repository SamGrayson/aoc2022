import re

DIR_KEY = ["up", "right", "down", "left"]
CARROT_KEY = {"up": "^", "down": "v", "right": ">", "left": "<"}
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
DIR_SCORE = {"up": 3, "down": 1, "right": 0, "left": 2}


def turn(direction, turn):
    if turn == "R":
        new_direction_idx = (
            DIR_KEY.index(direction) + 1
            if DIR_KEY.index(direction) != len(DIR_KEY) - 1
            else 0
        )
    if turn == "L":
        new_direction_idx = (
            DIR_KEY.index(direction) - 1
            if DIR_KEY.index(direction) != 0
            else len(DIR_KEY) - 1
        )
    return DIR_KEY[new_direction_idx]


def get_next_step(direction, position):
    if direction == "right":
        return (position[0], position[1] + 1)
    if direction == "left":
        return (position[0], position[1] - 1)
    if direction == "up":
        return (position[0] - 1, position[1])
    if direction == "down":
        return (position[0] + 1, position[1])


def get_new_starting_position(grid, max_l, position, direction):
    if direction == "up":
        for r in range(len(grid) - 1, -1, -1):
            if grid[r][position[1]] != "@":
                return (r, position[1])
    if direction == "down":
        for r in range(0, len(grid) - 1):
            if grid[r][position[1]] != "@":
                return (r, position[1])
    if direction == "right":
        for r in range(0, max_l - 1):
            if grid[position[0]][r] != "@":
                return (position[0], r)
    if direction == "left":
        for r in range(max_l - 1, -1, -1):
            if grid[position[0]][r] != "@":
                return (position[0], r)


def part_1(max_length):

    step_input = []
    grid = []
    starting_point = None

    with open("Day 22/input.txt") as data:
        temp = data.read().splitlines()

        done_found = False
        for line in temp:
            if "DONE" in line:
                done_found = True
                continue

            # We aren't done with the grid yet, next line after DONE will be the input.
            if not done_found:
                new_line = []
                for i, c in enumerate(line):
                    if c == " ":
                        new_line.append("@")
                    else:
                        if not starting_point:
                            starting_point = (0, i)
                        new_line.append(c)

                if len(new_line) < max_length:
                    new_line = new_line + ["@"] * (max_length - len(new_line))

                grid.append(new_line)
            else:
                step_input = list(filter(None, re.split("(\d+)", line.strip())))

    current_direction = "right"
    current_position = starting_point
    for step in step_input:
        # If step is a digit (walk)
        if re.match("\d", step):
            for i in range(int(step)):
                # "Paint" the carrot
                grid[current_position[0]][current_position[1]] = CARROT_KEY[
                    current_direction
                ]
                next_step = get_next_step(current_direction, current_position)

                # If next step is @ or out of bounds, loop..
                if (
                    next_step[0] < 0
                    or next_step[1] < 0
                    or next_step[1] > max_length - 1
                    or next_step[0] > len(grid) - 1
                    or grid[next_step[0]][next_step[1]] == "@"
                ):
                    next_step = get_new_starting_position(
                        grid, max_length, current_position, current_direction
                    )

                # If next step is rock, we're done
                if grid[next_step[0]][next_step[1]] == "#":
                    break

                current_position = next_step
                continue

        # If step is not a digit (turn)
        if re.match("\D", step):
            current_direction = turn(current_direction, step)
            continue

    # ex: 1000 * 6 + 4 * 8 + 0
    score = (1000 * (current_position[0] + 1)) + (
        4 * (current_position[1] + 1) + DIR_SCORE[current_direction]
    )

    return score


res = part_1(max_length=150)

print(res)
