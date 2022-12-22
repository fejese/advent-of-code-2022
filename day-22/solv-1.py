#!/usr/bin/env python3

import re

from dataclasses import dataclass
from enum import Enum
from typing import List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class C:
    x: int
    y: int

    def add(self, other: "C") -> "C":
        return C(self.x + other.x, self.y + other.y)

    def move(self, direction: "Dir") -> "C":
        return self.add(direction.value)


class Dir(Enum):
    R: C = C(1, 0)
    D: C = C(0, 1)
    L: C = C(-1, 0)
    U: C = C(0, -1)

    def rot_r(self) -> "Dir":
        if self == Dir.R:
            return Dir.D
        if self == Dir.D:
            return Dir.L
        if self == Dir.L:
            return Dir.U
        if self == Dir.U:
            return Dir.R

    def rot_l(self) -> "Dir":
        if self == Dir.R:
            return Dir.U
        if self == Dir.U:
            return Dir.L
        if self == Dir.L:
            return Dir.D
        if self == Dir.D:
            return Dir.R

    @property
    def marker(self) -> str:
        if self == Dir.R:
            return ">"
        if self == Dir.U:
            return "^"
        if self == Dir.L:
            return "<"
        if self == Dir.D:
            return "V"


def step(grid: List[str], curr_dir: Dir, curr_pos: C, steps: int):
    for i in range(steps):
        # grid[curr_pos.y][curr_pos.x] = curr_dir.marker
        next_pos = curr_pos.move(curr_dir)
        # print(f"  raw next pos: {next_pos}")
        if curr_dir == Dir.L:
            if next_pos.x < 0 or grid[next_pos.y][next_pos.x] == " ":
                # print("  wrapping around going left")
                next_pos = C(len(grid[next_pos.x]) - 1, next_pos.y)
        elif curr_dir == Dir.R:
            if (
                next_pos.x >= len(grid[next_pos.y]) - 1
                or grid[next_pos.y][next_pos.x] == " "
            ):
                # print("  wrapping around going right")
                next_pos = C(0, next_pos.y)
        elif curr_dir == Dir.D:
            if next_pos.y >= len(grid) - 1 or grid[next_pos.y][next_pos.x] == " ":
                # print("  wrapping around going down")
                next_pos = C(next_pos.x, 0)
        elif curr_dir == Dir.U:
            if next_pos.y < 0 or grid[next_pos.y][next_pos.x] == " ":
                # print("  wrapping around going up")
                next_pos = C(next_pos.x, len(grid) - 1)

        # print(f"  next pos after wrapping: {next_pos}")
        while grid[next_pos.y][next_pos.x] == " ":
            next_pos = next_pos.move(curr_dir)
            # print(f"  next pos after skipping empty: {next_pos}")

        # print(f"  next pos after skipping empties: {next_pos}")

        if grid[next_pos.y][next_pos.x] == "#":
            # grid[curr_pos.y][curr_pos.x] = curr_dir.marker
            return curr_pos

        curr_pos = next_pos

    # grid[curr_pos.y][curr_pos.x] = curr_dir.marker
    return curr_pos


with open(INPUT_FILE_NAME, "r") as input_file:
    input_parts = input_file.read().split("\n\n")
    grid: List[str] = [line.rstrip() for line in input_parts[0].splitlines()]
    curr_pos = C(grid[0].find("."), 0)
    curr_dir = Dir.R
    instructions = re.findall(r"(\d+|\w)", input_parts[1].rstrip())


max_line_length = max(len(line) for line in grid)
grid = [[c for c in line + (" " * (max_line_length - len(line)))] for line in grid]

# print(instructions, grid)
print(curr_dir, curr_pos)

for instr in instructions:
    if instr.isnumeric():
        steps = int(instr)
        print(f"Stepping {steps} from {curr_pos} to dir {curr_dir}")
        curr_pos = step(grid, curr_dir, curr_pos, steps)
    else:
        if instr == "L":
            print(f"Turning left")
            curr_dir = curr_dir.rot_l()
        elif instr == "R":
            print(f"Turning right")
            curr_dir = curr_dir.rot_r()
        else:
            raise Exception(f"wat {instr}")
    print("  => ", curr_dir, curr_pos)


# print()
# for line in grid:
#     print("".join(line))
# print()

row = curr_pos.y + 1
col = curr_pos.x + 1
d = [d for d in Dir].index(curr_dir)
print(row, col, d)
print(row * 1000 + col * 4 + d)
