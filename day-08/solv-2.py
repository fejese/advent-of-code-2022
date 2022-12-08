#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    grid = [[int(h) for h in line.strip()] for line in input_file]

width = len(grid[0])
height = len(grid)

score_grid = [[0] * width for _ in range(height)]

for y in range(height):
    for x in range(width):
        ch = grid[y][x]
        # right
        rs = 0
        for xi in range(x + 1, width):
            rs += 1
            if grid[y][xi] >= ch:
                break
        if rs == 0:
            continue
        # left
        ls = 0
        for xi in range(x - 1, -1, -1):
            ls += 1
            if grid[y][xi] >= ch:
                break
        if ls == 0:
            continue
        # bottom
        bs = 0
        for yi in range(y + 1, height):
            bs += 1
            if grid[yi][x] >= ch:
                break
        if bs == 0:
            continue
        # top
        ts = 0
        for yi in range(y - 1, -1, -1):
            ts += 1
            if grid[yi][x] >= ch:
                break
        if ts == 0:
            continue

        score_grid[y][x] = ls * ts * rs * bs


for line in grid:
    print(line)
print()
for line in score_grid:
    print(line)
print()

print(max(max(line) for line in score_grid))
