"""
Pass sand down until it hits the top of the tunnel! The last row is now a row of rocks
"""


import numpy as np

np.set_printoptions(linewidth=500)


def get_line(x_l, y_l, x_r, y_r, min_x):
    line = []
    # X line is diff, return x straight line
    if x_l != x_r:
        line = list(np.linspace(x_l, x_r, abs(x_l - x_r) + 1, dtype=int))
        line = list(map(lambda x: [x - min_x, y_r], line))
    # Y line is diff, return y straight line
    elif y_l != y_r:
        line = list(np.linspace(y_l, y_r, abs(y_l - y_r) + 1, dtype=int))
        line = list(map(lambda x: [x_r - min_x, x], line))
    # No line? return the dot
    else:
        line.append(x_r, y_r)
    return line


def create_rock_matrix(rock_paths, matrix, min_x):
    # For each rock path - raw the rocks
    for path in rock_paths:
        # Draw rocks
        i = 0
        while i < len(path) - 1:
            rock_line = get_line(
                path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], min_x
            )
            for rock_coord in rock_line:
                matrix[rock_coord[1], rock_coord[0]] = "#"
            i += 1
    return matrix


def create_sand_points(coordinates, matrix, points=0, starting_x=0):
    air = "."
    rock = "#"
    sand = "o"
    new_coordinates = []
    # Create a new column that we'll add if we go out of bounds diagonally
    new_column = np.full((len(matrix), 1), ".")
    new_column[-1] = rock

    # Create new columns if we're going to be out of bounds. - then redo the point check
    # Create new column to the left
    if coordinates[1] - 1 < 0:
        starting_x += 1
        coordinates[1] = coordinates[1] + 1
        matrix = np.column_stack((new_column, matrix))
        return create_sand_points(coordinates, matrix, points, starting_x)
    # Create new column to the right
    if coordinates[1] + 1 >= len(matrix[0]) - 1:
        matrix = np.column_stack((matrix, new_column))
        return create_sand_points(coordinates, matrix, points, starting_x)

    # If the space below the coordinates is sand, we need to move the sand down a level.
    if matrix[coordinates[0] + 1][coordinates[1]] == air:
        new_coordinates = [coordinates[0] + 1, coordinates[1]]
    # If the space diagonally left is air, move the sand that way
    elif matrix[coordinates[0] + 1][coordinates[1] - 1] == air:
        new_coordinates = [coordinates[0] + 1, coordinates[1] - 1]
    # If the space diagonally right is air, move the sand that way
    elif matrix[coordinates[0] + 1][coordinates[1] + 1] == air:
        new_coordinates = [coordinates[0] + 1, coordinates[1] + 1]
    # If none of the spaces around are air, we need to go up 1 level.
    else:
        matrix[coordinates[0]][coordinates[1]] = sand
        points += 1
        # When the coordinates = the starting position, we're done.
        end = (coordinates[0], coordinates[1]) == (0, starting_x)
        return (points, matrix, starting_x, end)

    return create_sand_points(new_coordinates, matrix, points, starting_x)


def part_1():

    # Paths are coordinates of start -> end lines
    # Ex: 498,4 -> 498,6 -> 496,6 = [[498,4], [498,6], [496,6]]
    matrix = []
    paths = []
    # Create the bounds around the rocks
    # Going to use min_x later on to translate coordinates (might update later who knows.)
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    # Add 1 to accounts for padded column on the left.
    starting_x = 501
    with open("Day 14/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            line_points = line.split(" -> ")
            for i in range(len(line_points)):
                # x, y coordinates
                line_points[i] = list(
                    map(lambda x: int(x), (line_points[i].split(",")))
                )
                # Set max and min coordinates
                if line_points[i][0] < min_x or min_x == 0:
                    min_x = line_points[i][0]
                if line_points[i][1] < min_y or min_y == 0:
                    min_y = line_points[i][1]
                if line_points[i][0] > max_x or max_x == 0:
                    max_x = line_points[i][0]
                if line_points[i][1] > max_y or max_y == 0:
                    max_y = line_points[i][1]
            paths.append(line_points)

        x_len = max_x - min_x + 1
        y_len = max_y + 1
        # Adjusted x
        starting_x = starting_x - min_x
        starting_coords = [0, starting_x]

        # Create empty matrix of "air" (".") (pad 1 row and a column on each side)
        matrix = np.full((y_len + 1, x_len + 2), ".", dtype=str)

        # Add rock row to bottom of matrix
        rock_row = np.full((1, len(matrix[0])), "#", dtype=str)
        matrix = np.append(matrix, rock_row, axis=0)

        # Create rock lines (min_x - 1 pads 1 column to the left)
        matrix = create_rock_matrix(paths, matrix, min_x - 1)

        # Create sand points and return # of placed sand - recursivly (updates reference)
        top_reached = False
        total_points = 0
        while not top_reached:
            sand_points, _matrix, _starting_x, _top_reached = create_sand_points(
                starting_coords, matrix, points=0, starting_x=starting_x
            )
            matrix = _matrix
            starting_x = _starting_x
            starting_coords = [0, _starting_x]
            total_points += sand_points
            top_reached = _top_reached

        return (matrix, total_points)


# Matrix
res = part_1()
print(f"Total sand points: {res[1]}")
with open("Day 14/outfile_pt2.txt", "wb") as f:
    np.savetxt(f, res[0], fmt="%s", delimiter=", ")
