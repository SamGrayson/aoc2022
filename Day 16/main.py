from copy import deepcopy

# Track the complete scores
complete_scores = []


class Valve:
    def __init__(self, name, flow_rate, paths_pre=[], paths={}, open=False):
        self.name = name
        self.flow_rate = flow_rate
        self.open = open
        # Keep track of the paths before they are classes
        self.paths_pre = paths_pre
        self.paths = {}

    def generate_score_tree(self, time_passed, scores={}):
        if time_passed < 30:
            # Takes time to open.
            score_multiplier = 0 if self.open else (time_passed + 1)
            steps_taken = time_passed
            score = score_multiplier * self.flow_rate
            if self.name not in scores or scores[self.name]["steps"] >= steps_taken:
                scores[self.name] = {
                    "score": score,
                    "steps": steps_taken if self.flow_rate == 0 else steps_taken + 1,
                }
                for i, p in self.paths.items():
                    p.generate_score_tree(steps_taken + 1, scores)
            return scores
        # done
        else:
            return scores


class CaveSystem:
    def __init__(self, valves={}, time_passed=0, total_pressure=0, current_pressure=0):
        self.valves = valves
        self.time_passed = time_passed
        self.total_pressure = total_pressure
        self.current_valve: Valve = None
        self.flow_rate = 0
        self.path = []

    def generate_links(self):
        for v in self.valves.values():
            for p in v.paths_pre:
                v.paths[p] = self.valves[p]

    def run(self):
        scores = self.current_valve.generate_score_tree(self.time_passed, {})
        sorted_scores = list(filter(lambda x: x[1]["score"] > 0, scores.items()))
        # If there are still scores left > 0, keep going down.
        if sorted_scores:
            # If all we have is 0 score left, we are done
            for s in sorted_scores:
                new_cave_system = deepcopy(self)
                new_cave_system.valves[s[0]].open = True
                new_cave_system.time_passed = s[1]["steps"]
                new_cave_system.path.append(s[0])
                new_cave_system.current_valve = new_cave_system.valves[s[0]]
                new_cave_system.flow_rate = (
                    new_cave_system.valves[s[0]].flow_rate + self.flow_rate
                )
                # Get sum of past steps
                past_time = 0
                if self.path:
                    past_time = new_cave_system.time_passed - self.time_passed
                new_cave_system.total_pressure = new_cave_system.total_pressure + (
                    self.flow_rate * past_time
                )
                new_cave_system.run()
        else:
            self.total_pressure = self.total_pressure + (
                self.flow_rate * (30 - self.time_passed)
            )
            complete_scores.append(self)
        return complete_scores


def part_1():
    cave_system = CaveSystem()
    with open("Day 16/input.txt") as data:
        temp = data.read().splitlines()
        # Create the valves and add them to the cave system
        for line in temp:
            # Skip line in input file, just there for easier reading
            if "SKIP" in line:
                continue
            split = line.split(";")
            # 0 - valve, 1 - rate, 2 - paths
            [valve, rate, paths] = split
            v = Valve(
                valve.strip(),
                int(rate.strip()),
                paths.strip().split(","),
            )
            cave_system.valves[v.name] = v

    # Start the cave system, it'll recursively call more cave systems until there's complete paths
    cave_system.generate_links()
    cave_system.current_valve = cave_system.valves["AA"]
    cave_system.run()
    highest_score_first = sorted(
        complete_scores, key=lambda s: s.total_pressure, reverse=True
    )
    return highest_score_first[0].total_pressure


res = part_1()
print(res)
