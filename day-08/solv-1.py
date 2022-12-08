#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    grid = [[int(h) for h in line.strip()] for line in input_file]

width = len(grid[0])
height = len(grid)

visibility_grid = [[0] * width for _ in range(height)]

# horizontal checks by row
for y in range(height):
    # left to right
    m = -1
    for x in range(width):
        h = grid[y][x]
        if h > m:
            visibility_grid[y][x] = 1
            m = h
    # right to left
    m = -1
    for x in reversed(range(width)):
        h = grid[y][x]
        if h > m:
            visibility_grid[y][x] = 1
            m = h


# vertical checks by row
for x in range(width):
    # top to bottom
    m = -1
    for y in range(height):
        h = grid[y][x]
        if h > m:
            visibility_grid[y][x] = 1
            m = h
    # right to left
    m = -1
    for y in reversed(range(height)):
        h = grid[y][x]
        if h > m:
            visibility_grid[y][x] = 1
            m = h

for line in grid:
    print(line)
print()
for line in visibility_grid:
    print(line)
print()

print(sum(sum(line) for line in visibility_grid))
