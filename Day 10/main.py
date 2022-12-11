import numpy as np

np.set_printoptions(linewidth=500)


class Executable:
    def __init__(self, _type, cycles_to_complete, adjustment, completes_at=None):
        self.type = _type
        self.cycles_to_complete = cycles_to_complete
        self.adjustment = adjustment
        self.completes_at = completes_at


class Device:
    def __init__(self):
        self.cycles = 0
        self.x = 1
        self.queue = []
        self.progress = {}
        # Part 1 signal strength
        self.signal_strength = 0
        # CRT Requirements
        self.crt_printout = []
        self.crt_row = []
        self.mod_cycle = 0
        pass

    def add_to_queue(self, executable):
        self.queue.append(executable)

    def run_part_1(self):
        while len(self.queue) > 0 or len(self.progress.items()) > 0:
            # Check the cycles, should we add to the signal_strength
            self.cycles += 1

            if self.cycles % 40 == 20:
                self.signal_strength += self.cycles * self.x

            if len(self.queue) > 0 and not len(self.progress):
                executable = self.queue.pop(0)
                completes_at = self.cycles + executable.cycles_to_complete
                executable.completes_at = completes_at
                executables = self.progress.get(executable.completes_at, [])
                self.progress[completes_at] = executables + [executable]

            # If there are executions in progress, check if they are complete.
            if len(self.progress) > 0:
                executables = self.progress.get(self.cycles, None)
                if executables:
                    for e in executables:
                        self.x = self.x + e.adjustment
                    # Remove the executables
                    del self.progress[self.cycles]

        return self.signal_strength

    # CRT
    def run_part_2(self):
        while len(self.queue) > 0 or len(self.progress.items()) > 0:
            # Check the cycles, should we add to the signal_strength
            if self.x - 1 <= self.cycles - self.mod_cycle <= self.x + 1:
                self.crt_row.append("#")
            else:
                self.crt_row.append(".")

            self.cycles += 1

            if len(self.queue) > 0 and not len(self.progress):
                executable = self.queue.pop(0)
                completes_at = self.cycles + executable.cycles_to_complete
                executable.completes_at = completes_at
                executables = self.progress.get(executable.completes_at, [])
                self.progress[completes_at] = executables + [executable]

            # If there are executions in progress, check if they are complete.
            if len(self.progress) > 0:
                executables = self.progress.get(self.cycles, None)
                if executables:
                    for e in executables:
                        self.x = self.x + e.adjustment
                    # Remove the executables
                    del self.progress[self.cycles]

            if self.cycles % 40 == 0:
                self.crt_printout.append(self.crt_row)
                self.crt_row = []
                self.mod_cycle = self.cycles

        return np.matrix(self.crt_printout)


def run():
    handheld1 = Device()
    handheld2 = Device()

    with open("Day 10/input.txt") as data:
        temp = data.read().splitlines()
        for line in temp:
            split = line.split(" ")
            type = split[0]
            adjustment = int(split[1]) if len(split) == 2 else 0
            if type == "addx":
                cycles_to_complete = 1
            # For now noop
            else:
                cycles_to_complete = 0
            executable = Executable(
                type,
                cycles_to_complete,
                adjustment,
            )
            # Part 1
            handheld1.add_to_queue(executable)
            # Part 2
            handheld2.add_to_queue(executable)
        return handheld2.run_part_2()


res = run()
print(res)
