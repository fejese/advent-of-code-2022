#!/usr/bin/env python3

from collections import defaultdict

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

min_x = min_y = min_z = max_x = max_y = max_z = 0
grid = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        x, y, z = [int(c) for c in line.strip().split(",")]
        grid[z][y][x] = 1
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

# print(min_x, min_y, min_z, max_x, max_y, max_z)

# for zi in range(min_z, max_z + 1):
#     for yi in range(min_y, max_y + 1):
#         for xi in range(min_x, max_x + 1):
#             print(grid[zi][yi][xi], end="")
#         print()
#     print()
min_x -= 1
min_y -= 1
min_z -= 1
max_x += 1
max_y += 1
max_z += 1

dcoords = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]

grid[min_z][min_y][min_x] = 2
to_visit = [(min_x, min_y, min_z)]
while to_visit:
    to_visit_new = []
    for (xi, yi, zi) in to_visit:
        for dx, dy, dz in dcoords:
            x = xi + dx
            if x < min_x - 1 or x > max_x + 1:
                continue
            y = yi + dy
            if y < min_y - 1 or y > max_y + 1:
                continue
            z = zi + dz
            if z < min_z - 1 or z > max_z + 1:
                continue
            if grid[z][y][x] == 0:
                grid[z][y][x] = 2
                to_visit_new.append((x, y, z))
    to_visit = to_visit_new


open_sides = 0
for zi in range(min_z, max_z + 1):
    for yi in range(min_y, max_y + 1):
        for xi in range(min_x, max_x + 1):
            if grid[zi][yi][xi] != 1:
                continue

            for dx, dy, dz in dcoords:
                if grid[zi + dz][yi + dy][xi + dx] == 2:
                    open_sides += 1

print(open_sides)
