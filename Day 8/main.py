"""
30373
25512
65332
33549
35390
"""
# Import for easy transposing
import numpy as np
from functools import reduce


def tree_func():
    # Create a matrix?
    matrix = []
    total_visible_trees = 0
    top_scenic_score = 0

    # Check if char is bigger than list given (part_1)
    def tree_visible(c, list):
        return all(i < c for i in list)

    # Return how many trees are visible (part_2)
    def get_visible_trees(c, list):
        visible = 0
        for t in list:
            if t < c:
                visible += 1
            elif t >= c:
                visible += 1
                return visible
        return visible

    with open("Day 8/input.txt") as data:
        temp = data.read().splitlines()
        # Create Matrix
        for line in temp:
            matrix.append(list(line))
            pass

        matrix = np.array(matrix)
        matrix_transpose = matrix.transpose()

        # Matrix loop
        for row, d in enumerate(matrix):
            for col, c in enumerate(d):
                # If we're on the outside, go ahead and add as visible tree
                if (
                    row == 0
                    or col == 0
                    or row == matrix.shape[0] - 1
                    or col == matrix.shape[0] - 1
                ):
                    total_visible_trees += 1
                    continue

                # Get rows
                row_right = list(d[col : len(d)])
                row_right.pop(0)
                row_left = list(d[0:col])

                # Get columns
                column = matrix_transpose[col]
                column_bottom = list(column[row : len(d)])
                column_bottom.pop(0)
                column_top = list(column[0:row])

                # PART 1 -------------------------------------------
                # If tree is visible from any angle, add to the list
                is_visible = any(
                    [
                        tree_visible(c, row_left),
                        tree_visible(c, row_right),
                        tree_visible(c, column_top),
                        tree_visible(c, column_bottom),
                    ]
                )
                if is_visible:
                    total_visible_trees += 1

                # PART 2 -------------------------------------------
                visible_trees = [
                    get_visible_trees(c, reversed(row_left)),
                    get_visible_trees(c, row_right),
                    get_visible_trees(c, reversed(column_top)),
                    get_visible_trees(c, column_bottom),
                ]
                # Get & Set new top score if greater
                scenic_score = reduce(lambda x, y: x * y, visible_trees)
                top_scenic_score = (
                    scenic_score
                    if scenic_score > top_scenic_score
                    else top_scenic_score
                )

    # [part1, part2]
    return [total_visible_trees, top_scenic_score]


res = tree_func()
print(res)
