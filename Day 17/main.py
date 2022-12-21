"""
Tetris kinda

The tall, vertical chamber is exactly seven units wide. 
Each rock appears so that its left edge is two units away from the left wall
and its bottom edge is three units above the highest rock in the room 
(or the floor, if there isn't one).
"""

import numpy as np
from tqdm import tqdm

np.set_printoptions(linewidth=500)

# fmt: off
SHAPES = {
    "flat": [
        ["#", "#", "#", "#"],
    ],
    "plus": [
        [".", "#", "."],
        ["#", "#", "#"],
        [".", "#", "."]
    ],
    "elbow": [
        [".", ".", "#"],
        [".", ".", "#"],
        ["#", "#", "#"]
    ],
    "line": [
        ["#"],
        ["#"],
        ["#"],
        ["#"]
    ],
    "block": [
        ["#", "#"],
        ["#", "#"],
    ]
}
# fmt: on
COLLISION_CHARS = ["|", "-", "@"]

DIRECTION_MAP = {
    ">": "right",
    "<": "left",
    "v": "down",
}


class Shape:
    def __init__(self, shape):
        self.shape = shape
        self.collisions = []

    # Get starting share provided a y & x of the grid.
    def get_starting_row(self, y, x):
        grid_wrapper = np.full((len(self.shape), x), ".")
        # Set the initial edge locations.
        for y, row in enumerate(self.shape):
            for x, v in enumerate(row):
                grid_wrapper[y][x + 3] = v

        # Find positions of all of the collisions.
        for y in list(range(0, len(grid_wrapper))):
            for x, v in enumerate(grid_wrapper[y]):
                if v == "#":
                    self.collisions.append((y, x))

        # Add the right & left containers.
        col = np.full(len(self.shape), "|")
        grid_wrapper[:, 0] = col
        grid_wrapper[:, -1] = col

        return grid_wrapper


class Grid(object):
    edges = set()

    def __init__(self, y, x, highest_y=0, padding=3):
        self.grid = np.full((1, x + 2), "-")
        self.padding = padding
        self.highest_y = highest_y
        self.y = y
        self.x = x

    def set_edge_locations(self):
        self.edges = set()
        # Set the initial edge locations.
        for y, row in enumerate(self.grid):
            for x, v in enumerate(row):
                if v in COLLISION_CHARS:
                    self.edges.add((y, x))

    def add_starting_shape(self, new_row):
        # Add padding above the grid as needed between each shape.
        needed_padding = 3
        if len(self.grid) == 1:
            pass
        else:
            for y, row in enumerate(self.grid):
                if "@" in row:
                    break
                needed_padding -= 1

        if needed_padding > 0:
            new_arr = np.array(["."] * (self.x + 2))
            new_arr[0] = "|"
            new_arr[-1] = "|"
            padding = [new_arr] * needed_padding
            self.grid = np.append(padding, self.grid, axis=0)
        else:
            self.grid = self.grid[abs(needed_padding) :]
            needed_padding = 0

        # Add the starting shape to the top of the grid - make a new grid
        self.grid = np.append(new_row, self.grid, axis=0)

        # Loop through grid and set edge locations. - just easier to do this each time..
        self.set_edge_locations()

    def set_highest_rock_y(self):
        # Set the initial edge locations.
        for y, row in enumerate(self.grid):
            if "@" in row:
                self.highest_y = y
                break

    def set_collision(self, collisions):
        for (y, x) in collisions:
            self.grid[y][x] = "@"

    def move_shape(self, shape_collisions, direction):
        x_movement = 0
        y_movement = 0

        collisions = shape_collisions

        if direction == "right":
            x_movement = 1
        elif direction == "left":
            collisions.reverse()
            x_movement = -1
        elif direction == "down":
            y_movement = 1

        collision = False
        i = len(shape_collisions) - 1
        new_collisions = []
        while i >= 0:
            c = collisions[i]
            y = c[0]
            x = c[1]
            if (y + y_movement, x + x_movement) in self.edges:
                # Reset if we hit a collision.
                for c in new_collisions:
                    self.grid[c[0]][c[1]] = "."
                new_collisions = shape_collisions
                # Only collide (rest) if going down.
                if direction not in ["right", "left"]:
                    self.edges.update(shape_collisions)
                    collision = True
                break
            else:
                i -= 1
                self.grid[y][x] = "."
                self.grid[y + y_movement][x + x_movement] = "#"
                new_collisions.insert(0, (y + y_movement, x + x_movement))

        # Reverse the added collisiosn back to their default positions.
        if direction == "left" and not collision:
            new_collisions.reverse()

        return (new_collisions, collision)


def part_1(limit=2022):
    # Stopped Count
    stopped_count = 0

    # Get the input
    with open("Day 17/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            input_max = len(line)
            input_steps = [c for c in line]
            # For resetting if we reach the end of our input.
            input_copy = input_steps.copy()

    # Create the grid that will track and print
    main_grid = Grid(0, 7)

    # Create shape input
    shape_input = [
        Shape(SHAPES["flat"]),
        Shape(SHAPES["plus"]),
        Shape(SHAPES["elbow"]),
        Shape(SHAPES["line"]),
        Shape(SHAPES["block"]),
    ]

    # Loop through each of the shapes for movement.
    shape_i = 0
    for i in tqdm(range(limit)):
        if shape_i == 5:
            shape_i = 0
        shape = shape_input[shape_i]
        shape_i += 1
        # Create the new row based on the hight & width of the grid
        new_row = shape.get_starting_row(len(main_grid.grid), len(main_grid.grid[0]))
        # Add that new row the grid and update the edges - required to get starting positions set.
        main_grid.add_starting_shape(new_row)
        keep_going_dawg = True
        new_collisions = []
        while keep_going_dawg:
            collisions = new_collisions if new_collisions else shape.collisions

            # If input stpes ran out, start over.
            if not input_steps:
                input_steps = input_copy.copy()
            direction = input_steps.pop(0)

            (new_collisions, collided) = main_grid.move_shape(
                collisions, DIRECTION_MAP[direction]
            )
            collisions = new_collisions
            if collided:
                keep_going_dawg = False

            (new_collisions, collided) = main_grid.move_shape(new_collisions, "down")
            collisions = new_collisions
            if collided:
                main_grid.set_collision(collisions)
                main_grid.set_highest_rock_y()
                keep_going_dawg = False

    return len(main_grid.grid) - (main_grid.highest_y + 1)


res = part_1()
print(res)
