#!/usr/bin/env python3

import math

from collections import defaultdict
from typing import Dict, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


stacks: Dict[int, List[str]] = defaultdict(list)

with open(INPUT_FILE_NAME, "r") as input_file:
    parts = input_file.read().split("\n\n")
    top_lines = parts[0].splitlines()
    c = len(top_lines[-1].strip()) // 3

for row in range(len(top_lines) - 2, -1, -1):
    for stack in range(c):
        col = stack * 4 + 1
        try:
            char = top_lines[row][col]
        except IndexError:
            char = None
        if char and char != " ":
            stacks[stack + 1].append(char)

for instuction in parts[1].splitlines():
    print(stacks)
    print(instuction)
    _, count, _, src, _, dst = instuction.split(" ")
    count = int(count)
    src = int(src)
    dst = int(dst)
    try:
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())
    except IndexError:
        pass

print(stacks)

result = ""
for stack in range(1, len(stacks) + 1):
    result += stacks[stack].pop()

print(result)
