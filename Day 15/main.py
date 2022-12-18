import numpy as np
from tqdm import tqdm

# Calculating Manhattan Distance from Scratch
def manhattan_distance(sensor, beacon):
    return sum(abs(value1 - value2) for value1, value2 in zip(sensor, beacon))


def part_1(y_check=10):
    no_beacon_lines = set()
    sensor_beacon_pair = []
    sensors_and_beacons = set()
    with open("Day 15/input.txt") as data:
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


class SensorData:
    def __init__(self, man_distance, sensor, beacon, l, t, r, b):
        self.man_distance = man_distance
        self.beacon = beacon
        self.sensor = sensor
        self.l = l
        self.t = t
        self.r = r
        self.b = b


# Refactor to check inside of squares?
def part_2(check=20, chunk=10):
    # Store bottom and top points
    sensor_data = []
    sensor_beacon_pair = []
    sensors_and_beacons = set()
    man_distance = 0
    with open("Day 15/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            split = line.split("|")
            sensor_vals = split[0].split(",")
            beacon_vals = split[1].split(",")

            sensors_and_beacons.add((int(sensor_vals[0]), int(sensor_vals[1])))
            sensors_and_beacons.add((int(beacon_vals[0]), int(beacon_vals[1])))

            sensor_beacon_pair.append(
                {
                    "sensor": (int(sensor_vals[0]), int(sensor_vals[1])),
                    "beacon": (int(beacon_vals[0]), int(beacon_vals[1])),
                }
            )

    # For testing purposes
    # draw = np.full((50, 50), ".")

    # For each sensor, create the diamond around it and add that point to the list
    for i, pair in enumerate(sensor_beacon_pair):
        sensor = pair["sensor"]
        beacon = pair["beacon"]

        man_distance = manhattan_distance(sensor, beacon)

        # Create diamond coordinates - too slow?
        bottom = (sensor[0], sensor[1] + man_distance)
        top = (sensor[0], sensor[1] - man_distance)
        right = (sensor[0] + man_distance, sensor[1])
        left = (sensor[0] - man_distance, sensor[1])

        # Skip triangles that are clearly outside of the bounds
        if top[1] > check:
            continue
        if left[0] > check:
            continue
        if right[0] < 0:
            continue
        if bottom[0] < 0:
            continue

        sensor_data.append(
            SensorData(man_distance, sensor, beacon, left, top, right, bottom)
        )

    # Divide the grid into easier chunks. If the corners of the grid are within a sensor, we don't need to check it.
    non_contained_grids = []
    for x in tqdm(range(0, check + 1, chunk), ascii=True, desc="grid_creation"):
        for y in range(0, check + 1, chunk):
            top_left_corner = (x, y)
            top_right_corner = (x + chunk, y)
            bottom_right_corner = (x + chunk, y + chunk)
            bottom_left_corner = (x, y + chunk)
            contained = False
            for sd in sensor_data:
                if all(
                    [
                        manhattan_distance(sd.sensor, top_left_corner)
                        <= sd.man_distance,
                        manhattan_distance(sd.sensor, top_right_corner)
                        <= sd.man_distance,
                        manhattan_distance(sd.sensor, bottom_right_corner)
                        <= sd.man_distance,
                        manhattan_distance(sd.sensor, bottom_left_corner)
                        <= sd.man_distance,
                    ]
                ):
                    # We're good
                    contained = True
                    break
            else:
                if not contained:
                    # Store the top corner for grid looping
                    non_contained_grids.append(top_left_corner)
            if y == check - chunk:
                # we're at the end of the chunks.
                break
        if x == check - chunk:
            # we're at the end of the chunks.
            break

    print(f"Grid Length: {len(non_contained_grids)}")
    for grid in tqdm(non_contained_grids, ascii=True, desc="Grid Looping"):
        for x in range(grid[0], grid[0] + chunk + 1):
            for y in range(grid[1], grid[1] + chunk + 1):
                not_in_sensor_range_found = False
                p_in_diamond = False
                for sd in sensor_data:
                    if manhattan_distance(sd.sensor, (x, y)) <= sd.man_distance:
                        p_in_diamond = True
                        break
                if not p_in_diamond:
                    not_in_sensor_range_found = (x, y)
                    return not_in_sensor_range_found


# res = part_1(10)
res = part_2(4000000, 1000)
print(res)
