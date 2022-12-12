#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class Coord:
    x: int
    y: int


def get_neighbours(pos: Coord) -> List[Coord]:
    global H
    global W
    neighbours = []
    for dx in (-1, 0, 1):
        if pos.x + dx < 0 or pos.x + dx >= W:
            continue
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            if dx != 0 and dy != 0:
                continue
            if pos.y + dy < 0 or pos.y + dy >= H:
                continue
            neighbours.append(Coord(pos.x + dx, pos.y + dy))
    return neighbours


with open(INPUT_FILE_NAME, "r") as input_file:
    height_map: List[List[int]] = [
        [ord(ch) - ord("a") for ch in line.strip()] for line in input_file
    ]

W = len(height_map[0])
H = len(height_map)

start = None
end = None
for y in range(H):
    for x in range(W):
        if height_map[y][x] == ord("S") - ord("a"):
            start = Coord(x, y)
            height_map[y][x] = 0
            if end:
                break
        if height_map[y][x] == ord("E") - ord("a"):
            end = Coord(x, y)
            height_map[y][x] = ord("z") - ord("a")
            if start:
                break


# for line in height_map:
#     print(line)
# print()


distances_from_end = [[None] * W for _ in range(H)]
distances_from_end[end.y][end.x] = 0

changes = True
while changes:
    changes = False

    for y in range(H):
        for x in range(W):
            pos = Coord(x, y)
            dist = distances_from_end[pos.y][pos.x]
            height = height_map[pos.y][pos.x]
            # print("pos", pos, "dist", dist, "height", height)
            neighbours = get_neighbours(pos)
            for neighbour in neighbours:
                neighbour_dist = distances_from_end[neighbour.y][neighbour.x]
                neighbour_height = height_map[neighbour.y][neighbour.x]
                # print("neighbour", neighbour, "dist", neighbour_dist, "height", neighbour_height)
                if neighbour_dist is None:
                    continue
                if dist is not None and dist <= neighbour_dist + 1:
                    continue
                if neighbour_height > height + 1:
                    continue
                dist = neighbour_dist + 1
                distances_from_end[pos.y][pos.x] = dist
                changes = True
            # for line in distances_from_end:
            #     print(line)
            # print()

# for line in distances_from_end:
#     print(line)
# print()

print(distances_from_end[start.y][start.x])
