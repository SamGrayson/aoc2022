import numpy as np

# Calculating Manhattan Distance from Scratch
def manhattan_distance(sensor, beacon):
    return sum(abs(value1 - value2) for value1, value2 in zip(sensor, beacon))


def part_1(y_check=10):
    no_beacon_lines = set()
    sensor_beacon_pair = []
    sensors_and_beacons = set()
    with open("Day 15/input_sample.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            split = line.split("|")
            sensor_vals = split[0].split(",")
            beacon_vals = split[1].split(",")

            sensors_and_beacons.add((int(sensor_vals[0]), int(sensor_vals[1])))
            sensors_and_beacons.add((int(beacon_vals[0]), int(beacon_vals[1])))

            sensor_beacon_pair.append(
                {
                    "sensor": [int(sensor_vals[0]), int(sensor_vals[1])],
                    "beacon": [int(beacon_vals[0]), int(beacon_vals[1])],
                }
            )

    # For each sensor, create the diamond around it and add that point to the list
    for pair in sensor_beacon_pair:
        sensor = pair["sensor"]
        beacon = pair["beacon"]
        man_distance = manhattan_distance(sensor, beacon)
        # Add the points of the square to the list.
        bottom_point = (sensor[0], sensor[1] + man_distance)
        top_point = (sensor[0], sensor[1] - man_distance)
        right_point = (sensor[0] + man_distance, sensor[1])
        left_point = (sensor[0] - man_distance, sensor[1])

        # Get all the lines
        down_right = list(
            zip(
                range(top_point[0] + 1, right_point[0]),
                range(top_point[1] + 1, right_point[1]),
            )
        )
        down_left = list(
            zip(
                range(top_point[0] - 1, left_point[0], -1),
                range(top_point[1] + 1, left_point[1]),
            )
        )
        up_right = list(
            zip(
                range(bottom_point[0] + 1, right_point[0]),
                range(bottom_point[1] - 1, right_point[1], -1),
            )
        )
        up_left = list(
            zip(
                range(top_point[0] - 1, left_point[0], -1),
                range(bottom_point[1] - 1, left_point[1], -1),
            )
        )

        for coord in (
            down_right
            + down_left
            + up_right
            + up_left
            + [bottom_point, top_point, left_point, right_point]
        ):
            if coord[1] == y_check and (coord[0], coord[1]) not in sensors_and_beacons:
                no_beacon_lines.add((coord[0], coord[1]))

    # Create line between far left and far right points
    line = sorted(no_beacon_lines)
    line_amt = abs(line[0][0]) + abs(line[-1][0])
    return line_amt


def part_2(x_check=20, y_check=20):
    no_beacon_lines = {}
    sensor_beacon_pair = []
    sensors_and_beacons = set()
    with open("Day 15/input_sample.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            split = line.split("|")
            sensor_vals = split[0].split(",")
            beacon_vals = split[1].split(",")

            sensors_and_beacons.add((int(sensor_vals[0]), int(sensor_vals[1])))
            sensors_and_beacons.add((int(beacon_vals[0]), int(beacon_vals[1])))

            sensor_beacon_pair.append(
                {
                    "sensor": [int(sensor_vals[0]), int(sensor_vals[1])],
                    "beacon": [int(beacon_vals[0]), int(beacon_vals[1])],
                }
            )

    # For each sensor, create the diamond around it and add that point to the list
    for pair in sensor_beacon_pair:
        sensor = pair["sensor"]
        beacon = pair["beacon"]
        man_distance = manhattan_distance(sensor, beacon)
        # Add the points of the square to the list.
        bottom_point = (sensor[0], sensor[1] + man_distance)
        top_point = (sensor[0], sensor[1] - man_distance)
        right_point = (sensor[0] + man_distance, sensor[1])
        left_point = (sensor[0] - man_distance, sensor[1])

        # Get all the lines
        down_right = list(
            zip(
                range(top_point[0] + 1, right_point[0]),
                range(top_point[1] + 1, right_point[1]),
            )
        )
        down_left = list(
            zip(
                range(top_point[0] - 1, left_point[0], -1),
                range(top_point[1] + 1, left_point[1]),
            )
        )
        up_right = list(
            zip(
                range(bottom_point[0] + 1, right_point[0]),
                range(bottom_point[1] - 1, right_point[1], -1),
            )
        )
        up_left = list(
            zip(
                range(top_point[0] - 1, left_point[0], -1),
                range(bottom_point[1] - 1, left_point[1], -1),
            )
        )

        for coord in (
            down_right
            + down_left
            + up_right
            + up_left
            + [bottom_point, top_point, left_point, right_point]
        ):
            if (
                0 <= coord[1] <= y_check
                and (coord[0], coord[1]) not in sensors_and_beacons
            ):
                new_line = no_beacon_lines.get(coord[1], set())
                new_line.add(coord)
                no_beacon_lines[coord[1]] = new_line

        print(no_beacon_lines[coord[1]])

    for k, l in no_beacon_lines.items():
        # Create line between far left and far right points
        l = sorted(l)
        # If outside the bounds of the check, the line is good
        line = sorted(l)
        line_amt = abs(line[0][0]) + abs(line[-1][0])
        print(line_amt)


# res = part_1(10)
res = part_2()
print(res)
