#!/usr/bin/env python3

import re
from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


# SELECTED_LINE_NO: int = 10
# INPUT_FILE_NAME: str = "test-input"
SELECTED_LINE_NO: int = 2000000
INPUT_FILE_NAME: str = "input"

LINE_PATTERN: re.Pattern = re.compile(
    r".*x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): .* x=(?P<bx>-?\d+), y=(?P<by>-?\d+)"
)


class S(Enum):
    EMPTY: str = "."
    BEACON: str = "B"
    SENSOR: str = "S"
    COVERED: str = "#"


Grid = Dict[int, Dict[int, S]]


@dataclass
class GridLimits:
    min_x: Optional[int] = None
    max_x: Optional[int] = None

    @property
    def min_y(self) -> int:
        return SELECTED_LINE_NO

    @property
    def max_y(self) -> int:
        return SELECTED_LINE_NO

    def update(self, points: List[Tuple[int, int]]) -> "GridLimits":
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        return GridLimits(
            min_x=min_x if self.min_x is None else min(self.min_x, min_x),
            max_x=max_x if self.max_x is None else max(self.max_x, max_x),
        )


def print_grid(grid: Grid, grid_limits: GridLimits) -> None:
    for y in range(grid_limits.min_y, grid_limits.max_y + 1):
        print(
            "".join(
                [
                    grid[y].get(x, S.EMPTY).value
                    for x in range(grid_limits.min_x, grid_limits.max_x + 1)
                ]
            )
        )
    print()


grid: Grid = defaultdict(lambda: defaultdict(lambda: S.EMPTY))
grid_limits: GridLimits = GridLimits()

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        print(f"processing {line.strip()}")
        match = LINE_PATTERN.match(line)
        assert match, line
        sx, sy, bx, by = [int(s) for s in match.groups()]
        grid[sy][sx] = S.SENSOR
        grid[by][bx] = S.BEACON
        d = abs(sy - by) + abs(sx - bx)
        dy = abs(SELECTED_LINE_NO - sy)
        if dy > d:
            continue
        grid_limits = grid_limits.update([(sx - d, sy), (sx + d, sy)])
        for xi in range(sx - d + dy, sx + d - dy + 1):
            if grid[SELECTED_LINE_NO][xi] == S.EMPTY:
                grid[SELECTED_LINE_NO][xi] = S.COVERED


print(grid_limits)
# print_grid(grid, grid_limits)
print(
    sum(
        1 if grid[SELECTED_LINE_NO][xi] == S.COVERED else 0
        for xi in range(grid_limits.min_x, grid_limits.max_x + 1)
    )
)
