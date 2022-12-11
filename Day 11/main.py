import functools
from typing import List


class Monkey:
    def __init__(self):
        self.inspected: int = 0
        self.starting_items: List[str] = []
        self.operation: str = ""
        self.test: int = ""
        self.if_true: str = ""
        self.if_false: str = ""


class MonkeyBusiness:
    def __init__(self, monkeys, lower_worry_levels=True):
        self.monkeys = monkeys
        self.lower_worry_levels = lower_worry_levels
        self.lcm = functools.reduce(
            lambda x, y: x * y, [m.test for k, m in monkeys.items()]
        )

    def process_item(self, item, monkey: Monkey):
        # Turn into an eval string
        operation = monkey.operation.replace("old", item)
        # Run the evaluation and divide by 3 once finshed if lower_worry_levels is true
        new_worry_level = (
            eval(operation) // 3 if self.lower_worry_levels else eval(operation)
        )
        # Check divisible worry
        # ex: 'divisible by 23'
        if new_worry_level % monkey.test == 0:
            # Move to monkey
            # ex: 'throw to monkey 2'
            self.monkeys[monkey.if_true].starting_items.append(
                str(new_worry_level % self.lcm)
            )
        else:
            # Move to monkey
            # ex: 'throw to monkey 3'
            self.monkeys[monkey.if_false].starting_items.append(
                str(new_worry_level % self.lcm)
            )

        # Remove the item from the list
        monkey.starting_items.pop(0)

        monkey.inspected += 1

    def process_round(self, round):
        # For each monkey, process all of its items and move around as needed.
        for k, monkey in self.monkeys.items():
            while len(monkey.starting_items) > 0:
                self.process_item(monkey.starting_items[0], monkey)


def parse_monkeys(lower_worry_levels=True):
    with open("Day 11/input.txt") as data:
        temp = data.read().splitlines()
        monkeys = {}
        current_monkey = None
        for line in temp:
            # Ignore ''
            if not line:
                continue

            # New monkey needs to be created
            if "Monkey" in line:
                split = line.split(" ")
                monkey_idx = split[1].replace(":", "")
                monkeys[monkey_idx] = Monkey()
                current_monkey = monkeys[monkey_idx]
                continue

            # Need to add item to current monkey dict
            split = line.strip().split(":")
            value = split[1].strip()
            # Key mapper
            if split[0].strip() == "Starting items":
                value = value.split(",")
                current_monkey.starting_items = value
            if split[0].strip() == "Operation":
                value = value.split("=")[1].strip()
                current_monkey.operation = value
            if split[0].strip() == "Test":
                value = value.split(" ")[-1].strip()
                current_monkey.test = int(value)
            if split[0].strip() == "If true":
                value = value.split(" ")[-1].strip()
                current_monkey.if_true = value
            if split[0].strip() == "If false":
                value = value.split(" ")[-1].strip()
                current_monkey.if_false = value

        business = MonkeyBusiness(monkeys, lower_worry_levels)

        return business


def part_1(rounds=20):
    business = parse_monkeys()

    for i in range(rounds):
        business.process_round(i)

    inspected = [
        {"monkey": k, "inspected": m.inspected} for k, m in business.monkeys.items()
    ]

    return sorted(inspected, key=lambda x: x["inspected"], reverse=True)


def part_2(rounds=100):
    business = parse_monkeys(lower_worry_levels=False)

    for i in range(rounds):
        business.process_round(i)

    inspected = [
        {"monkey": k, "inspected": m.inspected} for k, m in business.monkeys.items()
    ]

    return sorted(inspected, key=lambda x: x["inspected"], reverse=True)


# res = part_1()
res = part_2(10000)
print(res[0]["inspected"] * res[1]["inspected"])
