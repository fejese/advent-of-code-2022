#!/usr/bin/env python3

from enum import Enum
from dataclasses import dataclass
from typing import Set, Collection, Sequence


# TEST: bool = True
TEST: bool = False
INPUT_FILE_NAME: str = "test-input" if TEST else "input"
SHAPE_COUNT: int = 2022
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
        self.grid: List[List[S]] = [
            [S.EMPTY] * WIDTH for _ in range(SHAPE_COUNT * 4 + 20)
        ]

    @property
    def next_shape_idx(self) -> int:
        if self.last_shape_idx is None:
            return 0
        return (self.last_shape_idx + 1) % len(self.shapes)

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

            # print(self.wind_index, dx, can_move_sideways, parts_to_check)
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
                break

    def print(self) -> None:
        print("---")
        for i in reversed(range(self.height + 1)):
            print("".join([s.value for s in self.grid[i]]))
        print("---")
        print()


with open(INPUT_FILE_NAME, "r") as input_file:
    winds = input_file.read().strip()

shapes: Sequence[Shape] = [
    # -
    Shape(
        outer_parts=[C(i, 0) for i in range(4)],
        left_parts=[C(0, 0)],
        right_parts=[C(3, 0)],
        bottom_parts=[C(i, 0) for i in range(4)],
    ),
    # +
    Shape(
        outer_parts=[C(1, 0), C(0, 1), C(1, 1), C(1, 2), C(2, 1)],
        left_parts=[C(1, 0), C(1, 2), C(0, 1)],
        right_parts=[C(1, 0), C(1, 2), C(2, 1)],
        bottom_parts=[C(1, 0), C(0, 1), C(2, 1)],
    ),
    # _|
    Shape(
        outer_parts=[C(0, 0), C(1, 0), C(2, 0), C(2, 1), C(2, 2)],
        left_parts=[C(0, 0), C(2, 1), C(2, 2)],
        right_parts=[C(2, i) for i in range(3)],
        bottom_parts=[C(i, 0) for i in range(3)],
    ),
    # |
    Shape(
        outer_parts=[C(0, i) for i in range(4)],
        left_parts=[C(0, i) for i in range(4)],
        right_parts=[C(0, i) for i in range(4)],
        bottom_parts=[C(0, 0)],
    ),
    # []
    Shape(
        outer_parts=[C(i, j) for i in range(2) for j in range(2)],
        left_parts=[C(0, i) for i in range(2)],
        right_parts=[C(1, i) for i in range(2)],
        bottom_parts=[C(i, 0) for i in range(2)],
    ),
]

game = Game(winds, shapes)
# game.print()
for _ in range(SHAPE_COUNT):
    game.place_next_shape()
    # game.print()

print(game.height)
