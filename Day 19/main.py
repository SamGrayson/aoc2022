class Blueprint:
    def __init__(self, name: str):
        self.name = int(name)

    def set_ore_cost(self, ore_line: str):
        ore_line = ore_line.split("=")[1].split(" ")
        self.ore_cost = {}
        self.ore_cost[ore_line[1]] = int(ore_line[0])

    def set_clay_cost(self, clay_line: str):
        clay_line = clay_line.split("=")[1].split(" ")
        self.clay_cost = {}
        self.clay_cost[clay_line[1]] = int(clay_line[0])

    def set_obsidian_cost(self, obsidian_line: str):
        obsidian_line = obsidian_line.split("=")[1].split(",")
        mineral_costs = [l.split(" ") for l in obsidian_line]
        self.obsidian_cost = {}
        for l in mineral_costs:
            self.obsidian_cost[l[1]] = int(l[0])

    def set_geode_cost(self, geode_line: str):
        geode_line = geode_line.split("=")[1].split(",")
        mineral_costs = [l.split(" ") for l in geode_line]
        self.geode_cost = {}
        for l in mineral_costs:
            self.geode_cost[l[1]] = int(l[0])


class Factory:
    def __init__(self, blueprint: Blueprint):
        # Robot Costs
        self.ore_cost = blueprint.ore_cost
        self.clay_cost = blueprint.clay_cost
        self.obsidian_cost = blueprint.obsidian_cost
        self.geode_cost = blueprint.geode_cost

        # Mineral Amonunts
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0

        # Number of Robots
        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

        # Total Minutes Past
        self.minutes = 0

    def can_create_robot(self, _type) -> bool:
        can_create = True
        for k, v in getattr(self, f"{_type}_cost").items():
            if not getattr(self, k) >= v:
                can_create = False
        return can_create

    def create_robot(self, _type):
        # Remove the minerals to create a robot
        for k, v in getattr(self, f"{_type}_cost").items():
            mineral = getattr(self, k)
            robot = getattr(self, f"{_type}_robots")
            setattr(self, k, mineral - v)

    def next_cost(self, next_type, wait):
        can_create_next = True
        for k, v in getattr(self, f"{next_type}_cost").items():
            mineral = getattr(self, k)
            robots = getattr(self, f"{k}_robots")
            sim_mineral = mineral + (robots * wait)
            if not sim_mineral >= v:
                can_create_next = False
        return can_create_next

    def get_minerals(self):
        # Accumulate ore based on the number of robots we have.
        if self.ore_robots > 0:
            self.ore = self.ore + (self.ore_robots * 1)

        if self.clay_robots > 0:
            self.clay = self.clay + (self.clay_robots * 1)

        if self.obsidian_robots > 0:
            self.obsidian = self.obsidian + (self.obsidian_robots * 1)

        if self.geode_robots > 0:
            self.geode = self.geode + (self.geode_robots * 1)

    def run(self):
        while self.minutes < 24:
            add_robot = False
            # Create Robots if we can, we can to build geode -> osidian -> clay -> ore
            if self.can_create_robot("geode"):
                self.create_robot("geode")
                add_robot = "geode"
            elif self.can_create_robot("obsidian") and not self.next_cost("geode", 1):
                self.create_robot("obsidian")
                add_robot = "obsidian"
            elif (
                self.can_create_robot("clay")
                and not self.next_cost("obsidian", 2)
                and not self.next_cost("geode", 3)
            ):
                self.create_robot("clay")
                add_robot = "clay"
            elif (
                self.can_create_robot("ore")
                and not self.next_cost("clay", 1)
                and not self.next_cost("obsidian", 2)
                and not self.next_cost("geode", 3)
            ):
                self.create_robot("ore")
                add_robot = "ore"

            # Accumulate ore based on the number of robots we have.
            self.get_minerals()

            # Add the created robot in the end.
            if add_robot:
                setattr(
                    self,
                    f"{add_robot}_robots",
                    getattr(self, f"{add_robot}_robots") + 1,
                )

            self.minutes += 1


def part_1():

    blueprints = []
    scores = []

    with open("Day 19/input_sample.txt") as data:
        temp = data.read().splitlines()
        blueprint = None
        for line in temp:
            if "SKIP" in line:
                continue
            if "Blueprint" in line:
                if blueprint:
                    blueprints.append(blueprint)
                blueprint = Blueprint(line.split(" ")[1])
            if "ore_robot" in line:
                blueprint.set_ore_cost(line)
            if "clay_robot" in line:
                blueprint.set_clay_cost(line)
            if "obsidian_robot" in line:
                blueprint.set_obsidian_cost(line)
            if "geode_robot" in line:
                blueprint.set_geode_cost(line)
        else:
            blueprints.append(blueprint)

        for blueprint in blueprints:
            factory = Factory(blueprint)
            factory.run()
            scores.append(f"{blueprint.name * factory.geode}_{blueprint.name}")

    return sorted(scores, reverse=True)


res = part_1()
print(res)
