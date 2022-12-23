"""
  y
z   x
"""
from itertools import product

cubes = {}


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        # Coordinates are in z, y, x
        top_coordinates = [(z, y, x), (z, y, x - 1), (z - 1, y, x), (z - 1, y, x - 1)]
        bottom_coordinates = [
            (z - 1, y - 1, x - 1),
            (z, y - 1, x - 1),
            (z - 1, y - 1, x),
            (z - 1, y - 1, x - 1),
        ]
        self.coordinates = top_coordinates + bottom_coordinates
        # Get origins
        self.origins = [
            (self.z - 1, self.y, self.x - 1),
            (self.z, self.y - 1, self.x),
            (self.z, self.y, self.x),
            (self.z - 1, self.y - 1, self.x - 1),
        ]


def part_1(total_faces):

    blocked_points = set()
    all_points = set()
    cubes = []

    with open("Day 18/input_sample.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            split = line.split(",")
            cube = Cube(int(split[0]), int(split[1]), int(split[2]))
            for c in cube.coordinates:
                if c in all_points:
                    blocked_points.add(c)
                all_points.add(c)

            # Add the new cube
            cubes.append(cube)

    # Loop thourgh each cube, if the origin points are "blocked" it should be a cube
    contained_cube = []

    for c in blocked_points:
        new_cube = Cube(c[2], c[1], c[0])
        if all([o in blocked_points for o in new_cube.coordinates]):
            contained_cube.append(c)

    return total_faces - (len(contained_cube) * 6)


# Total faces from part 1 passed in for calculations
res = part_1(64)
print(res)
