import math
import numpy


def out_of_bounds(t_row, t_col, h_row, h_col):
    tail_location = [t_row, t_col]
    # Create 1 tile grid aroudn row and check if there.
    # x x x
    # x n x
    # x x x
    row_check = [
        [h_row + 1, h_col - 1],
        [h_row + 1, h_col],
        [h_row + 1, h_col + 1],
        [h_row, h_col - 1],
        [h_row, h_col],  # Can be on top of each over
        [h_row, h_col + 1],
        [h_row - 1, h_col - 1],
        [h_row - 1, h_col],
        [h_row - 1, h_col + 1],
    ]
    return tail_location not in row_check


def part_1():
    # row, col
    head_position = "0,0"
    tail_position = "0,0"
    unique_tail_locations = set(["0,0"])
    with open("Day 9/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            # R 2
            # options: L-eft R-ight U-p D-down
            head_row = int(head_position.split(",")[0])
            head_col = int(head_position.split(",")[1])
            tail_row = int(tail_position.split(",")[0])
            tail_col = int(tail_position.split(",")[1])

            direction = line.split(" ")[0].lower()
            move = int(line.split(" ")[1])

            for i in range(1, move + 1):
                if direction == "r":
                    head_col += 1
                elif direction == "l":
                    head_col -= 1
                elif direction == "u":
                    head_row += 1
                elif direction == "d":
                    head_row -= 1

                head_position = ",".join([str(head_row), str(head_col)])

                if out_of_bounds(tail_row, tail_col, head_row, head_col):
                    # If tail is out of bounds, move behind head
                    if direction == "r":
                        tail_col = head_col - 1
                        tail_row = head_row
                    elif direction == "l":
                        tail_col = head_col + 1
                        tail_row = head_row
                    elif direction == "u":
                        tail_col = head_col
                        tail_row = head_row - 1
                    elif direction == "d":
                        tail_col = head_col
                        tail_row = head_row + 1

                tail_position = ",".join([str(tail_row), str(tail_col)])

                unique_tail_locations.add(tail_position)

    return len(unique_tail_locations)


# ---- PART 2 ----


class Knot:
    def __init__(self, position, child=None, head=False, tail=False):
        self.position = position
        self.child = child
        self.head = head
        self.tail = tail

    def move(self, direction, parent_position=None):
        # If head, go ahead and move.
        if self.head:
            self.position = [
                self.position[0] + direction[0],
                self.position[1] + direction[1],
            ]
            self.child.move(direction, self.position)
        if parent_position and out_of_bounds(
            self.position[0], self.position[1], parent_position[0], parent_position[1]
        ):
            # Is parent in the same row or column?

            row_check = parent_position[0] - self.position[0]
            col_check = parent_position[1] - self.position[1]

            if row_check == 0 or col_check == 0:
                new_direction = None
                if row_check > 0 and col_check == 0:
                    self.position[0] += 1
                    new_direction = [1, 0]
                elif row_check < 0 and col_check == 0:
                    self.position[0] -= 1
                    new_direction = [-1, 0]
                elif row_check == 0 and col_check > 0:
                    self.position[1] += 1
                    new_direction = [0, 1]
                elif row_check == 0 and col_check < 0:
                    self.position[1] -= 1
                    new_direction = [0, -1]
                else:
                    print("why")

                # Add tail location to set - let the set figure out uniqueness
                if self.tail:
                    self.unique_tail_locations.add(
                        ",".join([str(self.position[0]), str(self.position[1])])
                    )

                if self.child:
                    self.child.move(new_direction, self.position)
            # No? Move Diagonally.
            else:
                """Diagonal movement"""
                northeast = [1, 1]
                northwest = [1, -1]
                southeast = [-1, 1]
                southwest = [-1, -1]

                new_direction = None
                if row_check > 0 and col_check > 0:
                    self.position[0] += 1
                    self.position[1] += 1
                    new_direction = northeast
                elif row_check < 0 and col_check < 0:
                    self.position[0] -= 1
                    self.position[1] -= 1
                    new_direction = southwest
                elif row_check < 0 and col_check > 0:
                    self.position[0] -= 1
                    self.position[1] += 1
                    new_direction = southeast
                elif row_check > 0 and col_check < 0:
                    self.position[0] += 1
                    self.position[1] -= 1
                    new_direction = northwest
                else:
                    print("why")

                # Add tail location to set - let the set figure out uniqueness
                if self.tail:
                    self.unique_tail_locations.add(
                        ",".join([str(self.position[0]), str(self.position[1])])
                    )

                if self.child:
                    self.child.move(new_direction, self.position)


class Rope:
    def __init__(self, knot_count):
        self.knots = []
        # Create list of knots
        for i in range(knot_count):
            self.knots.append(Knot([0, 0]))

        # Assign parent & child relationships (loop backwards) (messy but idk...)
        for i in range(len(self.knots) - 1, -1, -1):
            # tail - doesn't have child to contiue after
            if i == len(self.knots) - 1:
                self.knots[i].tail = True
                self.knots[i].unique_tail_locations = set(["0,0"])
                continue
            if i == 0:
                self.knots[i].head = True
            self.knots[i].child = self.knots[i + 1]

    def move_rope(self, direction, distance):
        for i in range(distance):
            if direction == "r":
                self.knots[0].move([0, 1])
            elif direction == "l":
                self.knots[0].move([0, -1])
            elif direction == "u":
                self.knots[0].move([1, 0])
            elif direction == "d":
                self.knots[0].move([-1, 0])

    def print_rope(self):
        print(numpy.array([k.position for k in self.knots]))
        print("------")


def part_2():
    # row, col
    rope = Rope(10)

    with open("Day 9/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            # R 2
            direction = line.split(" ")[0].lower()
            move = int(line.split(" ")[1])

            rope.move_rope(direction, move)
            rope.print_rope()

    return len(rope.knots[-1].unique_tail_locations)


res = part_2()
print(res)
