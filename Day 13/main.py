from ast import literal_eval


class Section(object):
    def __init__(self, left, right, section_number=None):
        self.left = left
        self.right = right
        self.section_number = section_number

    def is_valid(self, left, right):
        for i in range(max(len(left), len(right))):

            if i > (len(left) - 1):
                # "Right is bigger, were good"
                return True
            if i > (len(right) - 1):
                # "Right is smaller, bad"
                return False

            left_element = left[i]

            right_element = right[i]

            # If the elements don't equal each other - make sure they're both arrays
            if type(left_element) != type(right_element):
                left_element = (
                    [left_element] if type(left_element) is not list else left_element
                )
                right_element = (
                    [right_element]
                    if type(right_element) is not list
                    else right_element
                )

            # If list keep going, else do a check
            if type(left_element) is list and type(right_element) is list:
                # If we made it to the end of the list - skip to the next check
                valid = self.is_valid(left_element, right_element)
                if valid == "skip":
                    continue
                else:
                    return valid
            elif right_element < left_element:
                return False
            elif right_element > left_element:
                return True
        # Made it to the end of the list with no decision - skip and keep going.
        return "skip"

    def compare_sections(self):
        valid = self.is_valid(self.left, self.right)
        # If we skipped continuously - that is a valid entry
        if valid == "skip":
            return True
        else:
            return valid


def part_1():
    eval_list = []
    with open("Day 13/input.txt") as data:
        temp = data.read().splitlines()

        left = None
        right = None
        l = 0
        for line in temp:
            if left == None:
                left = literal_eval(line)
            elif right == None:
                right = literal_eval(line)
            else:
                l += 1
                eval_list.append(Section(left, right, l))
                left = None
                right = None

    results = {}
    for i, s in enumerate(eval_list):
        # Returns null if valid / false if invalid
        compared = s.compare_sections()
        results[i + 1] = compared

    return sum([k for k, i in results.items() if i])


def part_2():
    eval_list = []
    with open("Day 13/input.txt") as data:
        temp = data.read().splitlines()

        for line in temp:
            if line:
                eval_list.append(literal_eval(line))

        # Keys we'll be looking for
        eval_list.append([[2]])
        eval_list.append([[6]])

    # Bublee sort
    for i in range(0, len(eval_list) - 1):
        for j in range(len(eval_list) - 1):
            section = Section(eval_list[j], eval_list[j + 1])
            if not section.compare_sections():
                temp = eval_list[j]
                eval_list[j] = eval_list[j + 1]
                eval_list[j + 1] = temp

    key1 = eval_list.index([[2]]) + 1
    key2 = eval_list.index([[6]]) + 1
    return key1 * key2


res = part_2()
print(res)
