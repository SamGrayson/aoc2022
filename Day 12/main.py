import string
from collections import deque
from typing import List


class Node:
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val
        self.valid_neighbors = []
        self.in_queue = False

    def get_neighbors(self, num_map):
        x, y = self.pos
        p_paths = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
        for p in p_paths:
            if p in num_map:
                if num_map[p].val <= self.val + 1:
                    self.valid_neighbors.append(p)


class Solution:
    def __init__(self, num_map, starting_position, ending_position) -> None:
        self.num_map = num_map
        self.starting_position = starting_position
        self.ending_position = ending_position
        self.visited = set()
        self.queue = deque()

    # Little expensive - but helps not have duplicates in the queue.
    def reset_nodes(self):
        for v in self.num_map.values():
            v.in_queue = False

    def search_shortest(self, _starting_position=None):
        # push the root node to the queue and mark it as visited
        starting_position = (
            _starting_position if _starting_position else self.starting_position
        )
        self.queue.append([num_map[starting_position], 0])
        self.visited.add(starting_position)
        shortest_path = 0

        while self.queue:
            # If we're not at the top, get neighbors.
            [node, step] = self.queue.popleft()
            self.visited.add(node.pos)

            if node.pos == self.ending_position:
                shortest_path = step
                # Reset everything
                self.queue = deque()
                self.visited = set()
                self.reset_nodes()
                break

            for next_position in num_map[node.pos].valid_neighbors:
                node = num_map[next_position]
                if next_position not in self.visited and not node.in_queue:
                    node.in_queue = True
                    self.queue.append([node, step + 1])

        return shortest_path


def generate_alpha_map():
    map = {}
    for k, v in enumerate([*string.ascii_lowercase]):
        map[v] = k
    return map


alpha_map = generate_alpha_map()


def get_alpha_int(alpha):
    return alpha_map[alpha]


# Create num map instead of list
num_map = {}
starting_position = None
ending_position = None
with open("Day 12/input.txt") as data:
    temp = data.read().splitlines()
    line_row = 0
    for line in temp:
        for col, char in enumerate(line):
            if char == "S":
                starting_position = (line_row, col)
                val = 0
            elif char == "E":
                ending_position = (line_row, col)
                val = 25
            else:
                val = get_alpha_int(char.lower())
            num_map[(line_row, col)] = Node((line_row, col), val)
        line_row += 1

# Create neighbor mapping before execution.
for n in num_map:
    num_map[n].get_neighbors(num_map)


def part_1():
    solution = Solution(num_map, starting_position, ending_position)
    shortest_path = solution.search_shortest()
    return shortest_path


def part_2():
    # Get all the a nodes
    a_nodes = []
    for k, v in num_map.items():
        if v.val == 0:
            a_nodes.append(k)

    paths = []
    solution = Solution(num_map, starting_position, ending_position)
    # Get all of the paths from a, skip ones that can't make it to the end
    for n in a_nodes:
        steps = solution.search_shortest(n)
        if steps > 0:
            paths.append(steps)

    return min(paths)


res1 = part_1()
res2 = part_2()
print((res1, res2))
