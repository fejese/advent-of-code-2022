#!/bin/sh
"""'exec python3 -u -- "$0" ${1+"$@"} # """
# vi: syntax=python

from enum import Enum
from collections import defaultdict
from dataclasses import dataclass
from typing import Set, Collection, Sequence, Optional


# TEST: bool = True
TEST: bool = False
INPUT_FILE_NAME: str = "test-input" if TEST else "input"
# SHAPE_COUNT: int = 2022
SHAPE_COUNT: int = 1000000000000
WIDTH: int = 7


@dataclass
class C:
    x: int
    y: int


class S(Enum):
    EMPTY: str = "."
    ROCK: str = "#"


@dataclass
class Shape:
    outer_parts: Collection[C]
    left_parts: Collection[C]
    right_parts: Collection[C]
    bottom_parts: Collection[C]


class MovingShape:
    def __init__(self, shape: Shape, bottom_left: C):
        self.shape = shape
        self.bottom_left = bottom_left


class Game:
    def __init__(self, winds: str, shapes: Sequence[Shape]):
        self.winds = winds
        self.wind_index = 0
        self.shapes = shapes
        self.last_shape_idx = None
        self.height = 0
        self.grid: Dict[int, List[S]] = defaultdict(lambda: [S.EMPTY] * WIDTH)
        self.cache: Dict[str, Tuple[int, int]] = {}
        self.shapes_placed = 0

    @property
    def next_shape_idx(self) -> int:
        if self.last_shape_idx is None:
            return 0
        return (self.last_shape_idx + 1) % len(self.shapes)

    def get_cache_key(self) -> Optional[str]:
        cache_lines = 100
        if self.height <= cache_lines:
            return None
        key = f"{self.next_shape_idx}|{self.wind_index}"
        for h in range(max(0, self.height - 100), self.height + 1):
            key += "|"
            for i in range(WIDTH):
                key += self.grid[h][i].value

        return key

    def place_next_shape(self) -> None:
        next_shape_idx = self.next_shape_idx
        self.last_shape_idx = next_shape_idx
        shape = MovingShape(self.shapes[next_shape_idx], C(2, self.height + 3))

        while True:
            # apply wind
            dx = -1 if self.winds[self.wind_index] == "<" else 1
            self.wind_index = (self.wind_index + 1) % len(self.winds)
            can_move_sideways = True
            parts_to_check = (
                shape.shape.left_parts if dx < 0 else shape.shape.right_parts
            )
            for part in parts_to_check:
                new_x = part.x + shape.bottom_left.x + dx
                y = part.y + shape.bottom_left.y
                if new_x < 0 or new_x >= WIDTH:
                    can_move_sideways = False
                    break
                if self.grid[y][new_x] == S.ROCK:
                    can_move_sideways = False
                    break

            if can_move_sideways:
                shape.bottom_left = C(shape.bottom_left.x + dx, shape.bottom_left.y)

            # apply down move
            can_descent = True
            if shape.bottom_left.y == 0:
                can_descent = False
            else:
                for part in shape.shape.bottom_parts:
                    x = part.x + shape.bottom_left.x
                    new_y = part.y + shape.bottom_left.y - 1
                    if self.grid[new_y][x] == S.ROCK:
                        can_descent = False
                        break

            if can_descent:
                shape.bottom_left = C(shape.bottom_left.x, shape.bottom_left.y - 1)
            else:
                for part in shape.shape.outer_parts:
                    x = part.x + shape.bottom_left.x
                    y = part.y + shape.bottom_left.y
                    self.grid[y][x] = S.ROCK
                    self.height = max(self.height, y + 1)

                self.shapes_placed += 1
                return

    def place_n(self, n: int) -> int:
        cycle_length = None
        cycle_height = None
        while True:
            self.place_next_shape()
            key = self.get_cache_key()
            if self.shapes_placed == n:
                return self.height
            if key:
                if key in self.cache:
                    prev_shapes_placed, prev_height = self.cache[key]
                    cycle_length = self.shapes_placed - prev_shapes_placed
                    cycle_height = self.height - prev_height
                    break
                    print(key, self.cache[key], self.shapes_placed, self.height)
                self.cache[key] = (self.shapes_placed, self.height)

        full_cycles_left = (n - self.shapes_placed) // cycle_length
        shapes_left = n - full_cycles_left * cycle_length - self.shapes_placed
        for _ in range(shapes_left):
            self.place_next_shape()

        height = self.height + full_cycles_left * cycle_height
        return height

    def print(self) -> None:
        print("---")
        for i in reversed(range(self.height + 1)):
            print("".join([s.value for s in self.grid[i]]))
        print("---")
        print()


with open(INPUT_FILE_NAME, "r") as input_file:
    winds = input_file.read().strip()

shapes: Sequence[Shape] = [
    # [X] X  X  X
    Shape(
        outer_parts=[C(i, 0) for i in range(4)],
        left_parts=[C(0, 0)],
        right_parts=[C(3, 0)],
        bottom_parts=[C(i, 0) for i in range(4)],
    ),
    #     X
    #  X  X  X
    # [ ] X
    Shape(
        outer_parts=[C(1, 0), C(0, 1), C(1, 1), C(1, 2), C(2, 1)],
        left_parts=[C(1, 0), C(1, 2), C(0, 1)],
        right_parts=[C(1, 0), C(1, 2), C(2, 1)],
        bottom_parts=[C(1, 0), C(0, 1), C(2, 1)],
    ),
    #        X
    #        X
    # [X] X  X
    Shape(
        outer_parts=[C(0, 0), C(1, 0), C(2, 0), C(2, 1), C(2, 2)],
        left_parts=[C(0, 0), C(2, 1), C(2, 2)],
        right_parts=[C(2, i) for i in range(3)],
        bottom_parts=[C(i, 0) for i in range(3)],
    ),
    #  X
    #  X
    #  X
    # [X]
    Shape(
        outer_parts=[C(0, i) for i in range(4)],
        left_parts=[C(0, i) for i in range(4)],
        right_parts=[C(0, i) for i in range(4)],
        bottom_parts=[C(0, 0)],
    ),
    #  X  X
    # [X] X
    Shape(
        outer_parts=[C(i, j) for i in range(2) for j in range(2)],
        left_parts=[C(0, i) for i in range(2)],
        right_parts=[C(1, i) for i in range(2)],
        bottom_parts=[C(i, 0) for i in range(2)],
    ),
]

game = Game(winds, shapes)
print(game.place_n(SHAPE_COUNT))
