#!/usr/bin/env python3

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Set, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

W: int
H: int

Grid = Dict[complex, int]


@dataclass
class Blizzard:
    pos: complex
    direction: complex

    def __hash__(self) -> int:
        return int(
            self.pos.real * 10000
            + self.pos.imag * 100
            + self.direction.real * 10
            + self.direction.imag
        )


DNEIGHS: List[complex] = [
    dx + 1j * dy for dx in (1, 0, -1) for dy in (1, 0, -1) if dx * dy == 0
]


def print_grid(
    grid: Grid, blizzards: List[Blizzard], expedition: Optional[complex] = None
) -> None:
    to_print = []
    for y in range(H):
        row = []
        for x in range(W):
            coord = x + y * 1j
            row.append("#" if grid[coord] == -1 else ".")
        to_print.append(row)

    for blizzard in blizzards:
        prev_ch = to_print[int(blizzard.pos.imag)][int(blizzard.pos.real)]
        if prev_ch not in "#.":
            prev_count = int(prev_ch) if prev_ch.isnumeric() else 1
            ch = str(prev_count + 1)
        elif blizzard.direction.real < 0:
            ch = "<"
        elif blizzard.direction.real > 0:
            ch = ">"
        elif blizzard.direction.imag < 0:
            ch = "^"
        elif blizzard.direction.imag > 0:
            ch = "v"
        else:
            raise Exception(f"wat {blizzard}")

        to_print[int(blizzard.pos.imag)][int(blizzard.pos.real)] = ch

    if expedition is not None:
        to_print[int(expedition.imag)][int(expedition.real)] = "E"

    for line in to_print:
        print("".join(line))
    print()


def get_neighbours(pos: complex) -> List[complex]:
    global W, H
    return [
        dneigh + pos
        for dneigh in DNEIGHS
        if 0 <= int((dneigh + pos).real) < W and 0 <= int((dneigh + pos).imag) < H
    ]


def move_blizzards(
    grid: Grid, blizzards: List[Blizzard]
) -> Tuple[Grid, List[Blizzard]]:
    global W, H
    moved_blizzards: List[Blizzard] = []
    new_grid = deepcopy(grid)
    for blizzard in blizzards:
        new_grid[blizzard.pos] -= 1
        moved = replace(blizzard, pos=blizzard.pos + blizzard.direction)
        if moved.pos.real < 1:
            moved = replace(moved, pos=moved.pos + (W - 2))
        elif moved.pos.real > W - 2:
            moved = replace(moved, pos=moved.pos - (W - 2))
        elif moved.pos.imag < 1:
            moved = replace(moved, pos=moved.pos + 1j * (H - 2))
        elif moved.pos.imag > H - 2:
            moved = replace(moved, pos=moved.pos - 1j * (H - 2))

        new_grid[moved.pos] += 1
        moved_blizzards.append(moved)

    return new_grid, moved_blizzards


def find_shortest_path(
    grid: Grid, blizzards: List[Blizzard], start: complex, end: complex
) -> int:
    grid_states: List[Grid] = [grid]
    blizzard_states: List[List[Blizzard]] = [blizzards]

    print("Generating grid and blizzards states ...")
    new_grid, moved_blizzards = move_blizzards(grid, blizzards)
    while new_grid != grid_states[0]:
        grid_states.append(new_grid)
        blizzard_states.append(moved_blizzards)
        new_grid, moved_blizzards = move_blizzards(new_grid, moved_blizzards)
    assert moved_blizzards == blizzard_states[0]
    print("Done")

    states_to_visit: Set[complex] = set([start])
    visited: Set[Tuple[complex, int]] = set()
    pos_visited: Dict[complex, int] = defaultdict(int)
    step = 0
    while states_to_visit:
        next_step_mod = (step + 1) % len(grid_states)
        next_grid = grid_states[next_step_mod]

        new_states: Set[Tuple[complex, int]] = set()
        for curr_start in states_to_visit:
            if curr_start == end:
                return step

            if (curr_start, step) in visited:
                continue
            visited.add((curr_start, step))

            if pos_visited[curr_start] > 1000:
                continue
            pos_visited[curr_start]

            neighbours = get_neighbours(curr_start)
            if end in neighbours:
                return step + 1

            new_states.update(
                [
                    neigh
                    for neigh in neighbours
                    if ((neigh, next_step_mod) not in visited and next_grid[neigh] == 0)
                ]
            )

        # print(f"Step #{step}: {len(states_to_visit)} -> {len(new_states)}")
        states_to_visit = new_states
        step += 1


grid: Grid = {}
blizzards: List[Blizzard] = []

with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [line.strip() for line in input_file]
    H = len(lines)
    W = len(lines[0])
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            coord = x + 1j * y
            if ch == "#":
                grid[coord] = -1
            elif ch == ".":
                grid[coord] = 0
                if y == 0:
                    start = coord
                if y == len(lines) - 1:
                    end = coord
            else:
                grid[coord] = 1
                if ch == ">":
                    blizzards.append(Blizzard(coord, 1))
                elif ch == "v":
                    blizzards.append(Blizzard(coord, 1j))
                elif ch == "<":
                    blizzards.append(Blizzard(coord, -1))
                elif ch == "^":
                    blizzards.append(Blizzard(coord, -1j))

# print_grid(grid, blizzards)
shortest_path = find_shortest_path(grid, blizzards, start, end)
print(shortest_path)
