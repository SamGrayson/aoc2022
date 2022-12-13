import string


def generate_alpha_map():
    map = {}
    for k, v in enumerate([*string.ascii_lowercase]):
        map[v] = k
    return map


alpha_map = generate_alpha_map()


def get_alpha_int(alpha):
    return alpha_map[alpha]


class Solution:
    # Movement index
    up = [-1, 0]
    down = [1, 0]
    left = [0, -1]
    right = [0, 1]

    def __init__(self, num_matrix, starting_position, ending_position) -> None:
        self.complete_threads = []
        self.num_matrix = num_matrix
        self.starting_position = starting_position
        self.ending_position = ending_position

    def recursive_navigate(
        self,
        current_pos,
        thread,
    ):
        # If we made it to the end, we're done!
        if self.ending_position == [current_pos[0], current_pos[1]]:
            self.complete_threads.append(thread)
            return True

        # If we're not at the top of the grid, get the next position.
        current_val = self.num_matrix[current_pos[0]][current_pos[1]]

        # If we're not at the top of the grid, get the next position.
        if current_pos[0] != 0:
            new_row = current_pos[0] + self.up[0]
            new_col = current_pos[1] + self.up[1]
            new_top = [new_row, new_col]
            new_val = self.num_matrix[new_row][new_col]
            new_thread = thread + [new_top]
            if 0 <= new_val - current_val <= 1 and new_top not in thread:
                complete = self.recursive_navigate(new_top, new_thread)
                # if complete:
                #     return True

        # If we're not at the bottom of the grid, get the next position.
        if abs(current_pos[0]) != len(self.num_matrix) - 1:
            new_row = current_pos[0] + self.down[0]
            new_col = current_pos[1] + self.down[1]
            new_down = [new_row, new_col]
            new_val = self.num_matrix[new_row][new_col]
            new_thread = thread + [new_down]
            if 0 <= new_val - current_val <= 1 and new_down not in thread:
                complete = self.recursive_navigate(new_down, new_thread)
                # if complete:
                #     return True

        # If we're not at the left of the grid, get next position.
        if current_pos[1] != 0:
            new_row = current_pos[0] + self.left[0]
            new_col = current_pos[1] + self.left[1]
            new_left = [new_row, new_col]
            new_val = self.num_matrix[new_row][new_col]
            new_thread = thread + [new_left]
            if 0 <= new_val - current_val <= 1 and new_left not in thread:
                complete = self.recursive_navigate(new_left, new_thread)
                # if complete:
                #     return True

        # If we're not at the right of the grid, get next position.
        if current_pos[1] != len(self.num_matrix[0]) - 1:
            new_row = current_pos[0] + self.right[0]
            new_col = current_pos[1] + self.right[1]
            new_right = [new_row, new_col]
            new_val = self.num_matrix[new_row][new_col]
            new_thread = thread + [new_right]
            if 0 <= new_val - current_val <= 1 and new_right not in thread:
                complete = self.recursive_navigate(new_right, new_thread)
                # if complete:
                #     return True

        return False

    def run(self):
        print(".. Solution run() ..")
        self.recursive_navigate(self.starting_position, [self.starting_position])
        print("## Solution found! ##")


def part_1():
    num_matrix = []
    starting_position = [0, 0]
    ending_position = [0, 0]
    starting_num = -1

    with open("Day 12/input_sample.txt") as data:
        temp = data.read().splitlines()
        line_row = 0
        for line in temp:
            if "S" in line:
                starting_position = [line_row, line.index("S")]
            if "E" in line:
                ending_position = [line_row, line.index("E")]
            num_matrix.append([get_alpha_int(x.lower()) for x in line.strip()])
            line_row += 1
        num_matrix[starting_position[0]][starting_position[1]] = starting_num
        num_matrix[ending_position[0]][ending_position[1]] = get_alpha_int("z")

    solution = Solution(num_matrix, starting_position, ending_position)
    solution.run()

    return sorted([len(t) - 1 for t in solution.complete_threads])[0]


res = part_1()
print(res)
