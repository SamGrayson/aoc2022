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

    # A face will be all corners a cube
    def get_faces(self):
        # Start in the top y corner
        origin_one = str((self.z - 1, self.y, self.x - 1))
        self.origin_one = origin_one
        # middle, left. right - (reads left to right)
        face_g_1 = [
            origin_one + str((self.z, self.y, self.x)),
            str((self.z, self.y - 1, self.x - 1)) + origin_one,
            origin_one + str((self.z - 1, self.y - 1, self.x)),
        ]

        # Start in the diagonal bottom y corner
        origin_two = str((self.z, self.y - 1, self.x))
        self.origin_two = origin_two
        face_g_2 = [
            str((self.z - 1, self.y - 1, self.x - 1)) + origin_two,
            str((self.z, self.y, self.x - 1)) + origin_two,
            origin_two + str((self.z - 1, self.y, self.x)),
        ]
        return face_g_1 + face_g_2


def part_1():

    faces = set()
    touching_faces = set()

    with open("Day 18/input_sample.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            split = line.split(",")
            cube = Cube(int(split[0]), int(split[1]), int(split[2]))
            # If any of the faces are in the set, remove it
            c_faces = cube.get_faces()
            new_faces = []
            for f in c_faces:
                if f in faces:
                    print(f)
                    faces.remove(f)
                    touching_faces.add(f)
                else:
                    new_faces.append(f)

            # Add the new cube faces to the set
            faces.update(new_faces)

    return faces


res = part_1()
print(len(res))
