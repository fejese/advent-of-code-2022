#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

DIR_TO_VEC = {
    "D": (0, -1),
    "U": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def sign(n):
    if n == 0:
        return 0
    return n // abs(n)


def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def diff(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


def get_tail_move(H, T):
    d = diff(H, T)
    if abs(d[0]) <= 1 and abs(d[1]) <= 1:
        return (0, 0)

    return (sign(d[0]), sign(d[1]))


H = T = (0, 0)
visited = {T}
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        parts = line.split(" ")
        direction = DIR_TO_VEC[parts[0]]
        for _ in range(int(parts[1])):
            H = add(H, direction)
            move = get_tail_move(H, T)
            T = add(T, move)
            visited.add(T)
            print(H, T)

print(len(visited))
