from ast import literal_eval
from collections import OrderedDict
from tqdm import tqdm
import re


class MonkeyMath:
    def __init__(self, name, x, operator, y, aggregate_fn):
        self.name = name
        self.requirements = OrderedDict()
        self.requirements[x] = None
        self.requirements[y] = None
        self.operator = operator
        self.aggregate_fn = aggregate_fn
        pass

    def check(self, monkey_words, idx):
        # Check the words that have been yelled, do we need them in here?
        for k, v in self.requirements.items():
            if k in monkey_words.keys():
                self.requirements[k] = monkey_words[k]

        if all([v != None for v in list(self.requirements.values())]):
            requirements = list(self.requirements.values())
            x = requirements[0]
            y = requirements[1]
            if self.name == "root" and x != y:
                return "low" if x < y else "high"
            elif self.name == "root":
                return "YAS"
            eval_str = f"{x} {self.operator} {y}"
            val = eval(eval_str)
            self.aggregate_fn(self.name, val, idx)


OPERATIONS = ["+", "-", "*", "/", "=="]


def part_1(input=None, name_check=None):

    monkey_math_queue = []
    monkey_words = {}

    def is_root(name, val, m_idx):
        # If the name is root, we're done
        if name == "root":
            if type(val) == bool and val == True:
                print(monkey_words["humn"])
                print(name)
                print(int(val))
                # Go ahead and stop
                exit(0)

        # If not, we need to add the new value to the beginning of the queue (temp)
        else:
            temp.insert(0, f"{name}: {val}")

            monkey_math_queue.pop(m_idx)

    with open("Day 21/input_pt2.txt") as data:
        temp = data.read().splitlines()
        while temp:
            line = temp.pop(0)
            if any([o in line for o in OPERATIONS]) and not re.search("\d", line):
                split = line.split(" ")
                # 0: name:
                # 1: x
                # 2: operator
                # 3: y
                monkey_math_queue.append(
                    MonkeyMath(
                        split[0].replace(":", ""), split[1], split[2], split[3], is_root
                    )
                )
            else:
                split = line.split(" ")
                word = split[0].replace(":", "")

                num = split[1]

                # Part 2 brute force :D
                if word == name_check and i:
                    num = str(input)

                monkey_words[word] = num

            m: MonkeyMath
            for i, m in enumerate(monkey_math_queue):
                result = m.check(monkey_words, i)
                if result:
                    return result


# Start at a number relatively closer, then we'll hone in.
check_start = 3000000000000
check_start_idx = len(str(check_start))

# We'll break eventually :D
while True:
    high_or_low = part_1(check_start, "humn")
    if high_or_low == "high":
        check_start += int("1".ljust(check_start_idx, "0"))
    elif high_or_low == "low":
        check_start -= int("1".ljust(check_start_idx, "0"))
        check_start_idx -= 1
    elif high_or_low == "YAS":
        print("++++ RESULT ++++")
        print(check_start)
        break


# res = part_1()
