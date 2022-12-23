#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple

# INPUT_FILE_NAME: str = "test-input-small"
# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


class S(Enum):
    EMPTY: str = "."
    ELF: str = "#"

    def __str__(self) -> str:
        return self.value


class D(Enum):
    NORTH: List[complex] = [dx + 1j for dx in (-1, 0, 1)]
    SOUTH: List[complex] = [dx - 1j for dx in (-1, 0, 1)]
    WEST: List[complex] = [-1 + dy * 1j for dy in (-1, 0, 1)]
    EAST: List[complex] = [1 + dy * 1j for dy in (-1, 0, 1)]

    @property
    def next(self) -> "D":
        if self == D.NORTH:
            return D.SOUTH
        if self == D.SOUTH:
            return D.WEST
        if self == D.WEST:
            return D.EAST
        if self == D.EAST:
            return D.NORTH


ALL_NEIGHS: List[complex] = [
    dx + dy * 1j for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0
]


@dataclass
class GridLimits:
    min: complex = 0
    max: complex = 0

    def update(self, c: complex) -> "GridLimits":
        return GridLimits(
            min=min(self.min.real, c.real) + 1j * min(self.min.imag, c.imag),
            max=max(self.max.real, c.real) + 1j * max(self.max.imag, c.imag),
        )

    @property
    def size(self) -> int:
        return int(
            (self.max.real - self.min.real + 1) * (self.max.imag - self.min.imag + 1)
        )


def print_grid(grid: Dict[complex, S], limits: GridLimits) -> None:
    for y in range(int(limits.max.imag), int(limits.min.imag) - 1, -1):
        for x in range(int(limits.min.real), int(limits.max.real) + 1):
            print(str(grid[x + 1j * y]), end="")
        print()
    print()


def get_proposals(
    grid: Dict[complex, S], limits: GridLimits, first_proposal_direction: D
) -> Dict[complex, int]:
    proposals: Dict[complex, int] = defaultdict(int)
    for y in range(int(limits.max.imag), int(limits.min.imag) - 1, -1):
        for x in range(int(limits.min.real), int(limits.max.real) + 1):
            current = x + 1j * y
            if grid[current] == S.EMPTY:
                continue

            all_neighs_empty = True
            for dneigh in ALL_NEIGHS:
                neigh = current + dneigh
                if grid[neigh] == S.ELF:
                    all_neighs_empty = False
                    break
            if all_neighs_empty:
                continue

            d = first_proposal_direction
            for d_attempts in range(4):
                neighs_empty = True
                for dneigh in d.value:
                    neigh = current + dneigh
                    if grid[neigh] == S.ELF:
                        neighs_empty = False
                        break
                if neighs_empty:
                    proposals[current + d.value[1]] += 1
                    break
                d = d.next
    return proposals


def move(
    grid: Dict[complex, S],
    proposals: Dict[complex, int],
    limits: GridLimits,
    first_proposal_direction: D,
) -> Tuple[Dict[complex, S], GridLimits]:
    new_grid: Dict[complex, S] = defaultdict(lambda: S.EMPTY)
    new_limits: GridLimits = GridLimits()
    for y in range(int(limits.max.imag), int(limits.min.imag) - 1, -1):
        for x in range(int(limits.min.real), int(limits.max.real) + 1):
            current = x + 1j * y
            if grid[current] == S.EMPTY:
                continue

            all_neighs_empty = True
            for dneigh in ALL_NEIGHS:
                neigh = current + dneigh
                if grid[neigh] == S.ELF:
                    all_neighs_empty = False
                    break
            if all_neighs_empty:
                new_limits = new_limits.update(current)
                new_grid[current] = S.ELF
                continue

            d = first_proposal_direction
            made_proposal = False
            for d_attempts in range(4):
                neighs_empty = True
                for dneigh in d.value:
                    neigh = current + dneigh
                    if grid[neigh] == S.ELF:
                        neighs_empty = False
                        break
                if neighs_empty:
                    moved = current + d.value[1]
                    if proposals[moved] == 1:
                        new_grid[moved] = S.ELF
                        new_grid[current] = S.EMPTY
                        new_limits = new_limits.update(moved)
                        made_proposal = True
                    break
                d = d.next
            if not made_proposal:
                new_limits = new_limits.update(current)
                new_grid[current] = S.ELF

    return new_grid, new_limits


grid: Dict[complex, S] = defaultdict(lambda: S.EMPTY)
grid_limits = GridLimits()
elf_count: int = 0

with open(INPUT_FILE_NAME, "r") as input_file:
    for y, line in enumerate(input_file):
        for x, ch in enumerate(line.strip()):
            pos = x - 1j * y
            status = S(ch)
            grid[pos] = status
            grid_limits = grid_limits.update(pos)
            if status == S.ELF:
                elf_count += 1


print("== Initial State ==")
print_grid(grid, grid_limits)

directions = [d for d in D]
for i in range(10):
    starting_direction = directions[i % len(directions)]
    proposals: Dict[complex, int] = get_proposals(grid, grid_limits, starting_direction)
    # print_grid(proposals, grid_limits)
    grid, grid_limits = move(grid, proposals, grid_limits, starting_direction)
    print(f"== End of Round {i + 1} ==")
    print_grid(grid, grid_limits)

grid_size = grid_limits.size
print("grid size:", grid_size)
print("elves:", elf_count)
print("empty:", grid_size - elf_count)
