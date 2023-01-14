import copy
import numpy as np

# Direction Vectors
VECTORS = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}

# Path Types
WALL = "#"
CLEAR = "."

# Store all the grid points for lookup. based on the minute
# { 0: { points: ...} }
grid_points = {}


def print_for_test(min):
    grid = np.full((GRID_HEIGHT + 1, GRID_WIDTH + 1), ".")
    for v in grid_points[min].values():
        if v.blizzards:
            if len(v.blizzards) == 1:
                grid[v.y][v.x] = v.blizzards[0]
            else:
                grid[v.y][v.x] = len(v.blizzards)
    print(grid)


# Track the grid and all it's neighbors for searching
class Point:
    is_wall = False

    def __init__(self, x, y, vector):
        self.x = x
        self.y = y
        self.adj = set()
        # Track the blizzards at the point.
        self.blizzards = []
        if vector == WALL:
            self.is_wall = True
        if vector in VECTORS.keys():
            self.blizzards.append(vector)

    def set_adjacent_ref(self, vectors, grid_points):
        for v in vectors.values():
            adj_point = grid_points.get(f"({self.x + v[0]},{self.y + v[1]})")
            if adj_point:
                self.adj.add(adj_point.__str__())

    def __str__(self):
        return f"({self.x},{self.y})"


# Look at each point in the given grid and if it's a dir vector, move the blizzard
def simluate_blizzards(_grid_points):
    # Need to refactor....
    new_grid = copy.deepcopy(_grid_points)

    for point in _grid_points.values():
        for blizzard in point.blizzards:
            movement = VECTORS[blizzard]
            new_x = point.x + movement[0]
            new_y = point.y + movement[1]
            # If the new blizzard point is a wall, wrap it around depending on the direction.
            if _grid_points[f"({new_x},{new_y})"].is_wall:
                if blizzard == ">":
                    new_x = 1
                    new_y = point.y + movement[1]
                if blizzard == "<":
                    new_x = GRID_WIDTH - 1
                    new_y = point.y + movement[1]
                if blizzard == "v":
                    new_x = point.x + movement[0]
                    new_y = 1
                if blizzard == "^":
                    new_x = point.x + movement[0]
                    new_y = GRID_HEIGHT - 1
            # Remove blizzard from the old position and add it to the new position
            new_grid[point.__str__()].blizzards.remove(blizzard)
            new_grid[f"({new_x},{new_y})"].blizzards.append(blizzard)

    return new_grid


visited = set()
queue = []
# Go to each next clear spot after simulating the blizzard and keep going till we can get to the end.
def find_shortest_path(start_point: Point, _minutes=0):
    # Set initial queue
    queue.append(start_point.__str__() + f"-{_minutes}")

    while queue:
        p = queue.pop(0)
        q_min = int(p.split("-")[1])
        coordinate = p.split("-")[0]
        # If we don't have a point mapping for the next time, simulate the blizzard for all points in the tree
        if not grid_points.get(q_min + 1, None):
            new_grid = simluate_blizzards(grid_points[q_min])
            grid_points[q_min + 1] = new_grid
            print(f"-- minute: {q_min}")
            # print_for_test(q_min + 1)

        # Get the grid point at the time given in the queue for the coordinate
        current_point = grid_points[q_min][coordinate]

        # Can we stay here safely?
        if not grid_points[q_min + 1][current_point.__str__()].blizzards:
            p_in_time = current_point.__str__() + f"-{q_min+1}"
            if p_in_time not in visited:
                queue.append(p_in_time)

        for adj in current_point.adj:
            # Check if point is the end
            if adj == ENDING_POINT:
                return q_min + 1
            adj_point = grid_points[q_min + 1][adj]
            p_in_time = adj + f"-{q_min+1}"
            if (
                p_in_time not in visited
                and not adj_point.blizzards
                and not adj_point.is_wall
            ):
                visited.add(p_in_time)
                queue.append(p_in_time)


def part_1():

    with open("Day 24/input.txt") as data:
        temp = data.read().splitlines()
        x = -1
        y = -1
        starting_grid = {}

        global GRID_HEIGHT
        GRID_HEIGHT = len(temp) - 1

        global GRID_WIDTH
        GRID_WIDTH = len(temp[0]) - 1

        # Set globals for lookup in functions
        global STARTING_POINT
        STARTING_POINT = f"(1,0)"

        global ENDING_POINT
        ENDING_POINT = f"({GRID_WIDTH-1},{GRID_HEIGHT})"

        for line in temp:
            x += 1
            y = -1
            for v in line:
                y += 1
                p = Point(y, x, v)
                starting_grid[p.__str__()] = p

    # Add the adj points to each grid point
    for p in starting_grid.values():
        p.set_adjacent_ref(VECTORS, starting_grid)

    grid_points[0] = starting_grid

    print("LETS GO!")
    shortest_time = find_shortest_path(
        STARTING_POINT,
    )

    return shortest_time


res = part_1()
print(res)
