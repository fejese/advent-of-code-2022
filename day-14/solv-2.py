#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum, auto
from collections import defaultdict
from typing import Dict, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class C:
    x: int
    y: int

    @staticmethod
    def from_str(s: str) -> "C":
        return C(*[int(part) for part in s.strip().split(",")])

    def get_dir(self, other: "C") -> "C":
        return C(
            x=max(min(other.x - self.x, 1), -1),
            y=max(min(other.y - self.y, 1), -1),
        )

    def add(self, other: "C") -> "C":
        return C(
            x=self.x + other.x,
            y=self.y + other.y,
        )


SOURCE: C = C(500, 0)


class S(Enum):
    EMPTY: str = "."
    ROCK: str = "#"
    SAND: str = "o"


Grid = Dict[int, Dict[int, S]]


@dataclass
class GridLimits:
    min_x: int = SOURCE.x
    max_x: int = SOURCE.x
    max_y: int = SOURCE.y

    @property
    def min_y(self) -> int:
        return 0

    def update(self, c: C) -> "GridLimits":
        return GridLimits(
            min_x=min(self.min_x, c.x),
            max_x=max(self.max_x, c.x),
            max_y=max(self.max_y, c.y),
        )


def draw_points(grid: Grid, grid_limits: GridLimits, points: List[C]) -> GridLimits:
    grid[points[0].y][points[0].x] = S.ROCK
    grid_limits = grid_limits.update(points[0])
    curr = points[0]
    for point in points[1:]:
        grid_limits = grid_limits.update(point)
        v = curr.get_dir(point)
        while True:
            curr = curr.add(v)
            grid[curr.y][curr.x] = S.ROCK
            if curr == point:
                break
    return grid_limits


def print_grid(grid: Grid, grid_limits: GridLimits) -> None:
    for y in range(grid_limits.max_y + 1):
        print(
            "".join(
                [
                    grid[y].get(x, S.EMPTY).value
                    for x in range(grid_limits.min_x - 1, grid_limits.max_x + 1)
                ]
            )
        )
    print()


def pour_sand(grid: Grid, grid_limits: GridLimits, source: C) -> int:
    count = 0
    while True:
        sand = source
        settled = False

        while not settled and sand.y < grid_limits.max_y:
            if grid[sand.y + 1].get(sand.x, S.EMPTY) == S.EMPTY:
                sand = sand.add(C(0, 1))
                continue
            if grid[sand.y + 1].get(sand.x - 1, S.EMPTY) == S.EMPTY:
                sand = sand.add(C(-1, 1))
                continue
            if grid[sand.y + 1].get(sand.x + 1, S.EMPTY) == S.EMPTY:
                sand = sand.add(C(1, 1))
                continue

            grid[sand.y][sand.x] = S.SAND
            settled = True
            count += 1

        if sand == source:
            break
    return count


grid: Grid = defaultdict(lambda: defaultdict(S))
grid_limits: GridLimits = GridLimits()


with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        points = [C.from_str(point) for point in line.strip().split(" -> ")]
        grid_limits = draw_points(grid, grid_limits, points)

grid_limits = draw_points(
    grid,
    grid_limits,
    [
        C(SOURCE.x - grid_limits.max_y - 2, grid_limits.max_y + 2),
        C(SOURCE.x + grid_limits.max_y + 2, grid_limits.max_y + 2),
    ],
)
print_grid(grid, grid_limits)

count = pour_sand(grid, grid_limits, SOURCE)
print_grid(grid, grid_limits)
print(count)
