#!/usr/bin/env python3

import re
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


# TEST: bool = True
TEST: bool = False

INPUT_FILE_NAME: str = "test-input" if TEST else "input"


@dataclass
class GridLimits:
    min_x: int = 0
    max_x: int = 20 if TEST else 4000000
    min_y: int = 0
    max_y: int = 20 if TEST else 4000000


@dataclass
class Sensor:
    x: int
    y: int
    d: int


LINE_PATTERN: re.Pattern = re.compile(
    r".*x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): .* x=(?P<bx>-?\d+), y=(?P<by>-?\d+)"
)

grid_limits: GridLimits = GridLimits()
sensors: List[Sensor] = []

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        print(f"processing {line.strip()}")
        match = LINE_PATTERN.match(line)
        assert match, line
        sx, sy, bx, by = [int(s) for s in match.groups()]
        d = abs(sy - by) + abs(sx - bx)
        sensors.append(Sensor(sx, sy, d))


print(grid_limits)
print(sensors)

found = False
y = grid_limits.min_y
while y <= grid_limits.max_y:
    x = grid_limits.min_x
    while x <= grid_limits.max_x:
        covered = False
        for s in sensors:
            d = abs(s.y - y) + abs(s.x - x)
            if d <= s.d:
                x += max(1, s.d - d)
                covered = True
                break
        if not covered:
            print()
            print((x, y), (x * 4000000 + y))
            found = True
            break
    if found:
        break
    if y % 100000 == 0:
        print(y)
    y += 1
