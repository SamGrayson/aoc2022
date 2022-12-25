import numpy as np


def is_elf_around(elf_location, elf_tracker, elf="#"):
    # Create 1 tile grid around row and check if elf is there.
    # x x x
    # x n x
    # x x x
    elf_row = elf_location[0]
    elf_col = elf_location[1]

    row_check = [
        (elf_row + 1, elf_col - 1) in elf_tracker,
        (elf_row + 1, elf_col) in elf_tracker,
        (elf_row + 1, elf_col + 1) in elf_tracker,
        (elf_row, elf_col - 1) in elf_tracker,
        (elf_row, elf_col + 1) in elf_tracker,
        (elf_row - 1, elf_col - 1) in elf_tracker,
        (elf_row - 1, elf_col) in elf_tracker,
        (elf_row - 1, elf_col + 1) in elf_tracker,
    ]
    return any(row_check)


def process_move(elf, movement, elf_tracker):

    if not is_elf_around(elf, elf_tracker):
        # DO NOTHING
        return

    for direction in movement:
        if direction == "north":
            # If an elf isn't in the location, propose moving there.
            if not any(
                [
                    (elf[0] - 1, elf[1] - 1) in elf_tracker,
                    (elf[0] - 1, elf[1]) in elf_tracker,
                    (elf[0] - 1, elf[1] + 1) in elf_tracker,
                ]
            ):
                return (elf[0] - 1, elf[1])

        if direction == "south":
            # If an elf isn't in the location, propose moving there.
            if not any(
                [
                    (elf[0] + 1, elf[1] - 1) in elf_tracker,
                    (elf[0] + 1, elf[1]) in elf_tracker,
                    (elf[0] + 1, elf[1] + 1) in elf_tracker,
                ]
            ):
                return (elf[0] + 1, elf[1])

        if direction == "east":
            # If an elf isn't in the location, propose moving there.
            if not any(
                [
                    (elf[0] - 1, elf[1] + 1) in elf_tracker,
                    (elf[0], elf[1] + 1) in elf_tracker,
                    (elf[0] + 1, elf[1] + 1) in elf_tracker,
                ]
            ):
                return (elf[0], elf[1] + 1)

        if direction == "west":
            # If an elf isn't in the location, propose moving there.
            if not any(
                [
                    (elf[0] - 1, elf[1] - 1) in elf_tracker,
                    (elf[0], elf[1] - 1) in elf_tracker,
                    (elf[0] + 1, elf[1] - 1) in elf_tracker,
                ]
            ):
                return (elf[0], elf[1] - 1)


def part_1(rounds):

    elf_tracker = set()
    movement = ["north", "south", "west", "east"]
    ELF_LOCATOR = "#"

    with open("Day 23/input.txt") as data:
        temp = data.read().splitlines()
        row = 0
        # Set Elf Locations
        for line in temp:
            col = 0
            for land in line:
                if land == ELF_LOCATOR:
                    elf_tracker.add((int(row), int(col)))
                col += 1
            row += 1

        completed_rounds = 0
        while rounds > 0:
            rounds -= 1
            # ROUND 1
            ## Track the next movement, only move if the next coordinate has 1 elf
            next_movement = {}
            for elf in elf_tracker:
                elf_movement = process_move(elf, movement, elf_tracker)
                next_movement[elf_movement] = next_movement.get(elf_movement, [])
                next_movement[elf_movement].append(elf)

            # ROUND 2
            ## Move the elf if there's only 1 elf thinking of the next move
            for location, elves in next_movement.items():
                # Some elves can't move so their key in NONE
                if not location:
                    if len(elves) == len(elf_tracker):
                        # If no elves can move, then we can exit
                        print(
                            f"-- ROUND {completed_rounds} COMPLETE NO ELVES CAN MOVE --"
                        )
                        exit(0)

                # Only consider movements with 1 elf.
                if len(elves) > 1:
                    continue

                # Should only be 1 elf.
                elf = elves[0]

                # Remove the previous location & add the new one.
                elf_tracker.remove(elf)
                elf_tracker.add(location)

            # ROUND 3
            ## Move the front location to the back of the list.
            movement.insert(len(movement) - 1, movement.pop(0))
            completed_rounds += 1

    # Create rectangle & check for empty rows
    row_sort = sorted(list(elf_tracker), key=lambda x: x[0], reverse=True)
    col_sort = sorted(list(elf_tracker), key=lambda x: x[1], reverse=True)
    # Add 1 to account for 0 index
    max_row = row_sort[0][0] + 1
    min_row = abs(row_sort[-1][0])
    max_col = col_sort[0][1] + 1
    min_col = abs(col_sort[-1][1])

    # Surface Area - The elves
    return (max_row + min_row) * (min_col + max_col) - len(elf_tracker)


res = part_1(rounds=float("inf"))
print(res)
