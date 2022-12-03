#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

S: int = 0


def get_priority(char: str) -> int:
    assert len(char) == 1
    assert char.isalpha()

    if char.islower():
        return ord(char) - ord("a") + 1

    return ord(char) - ord("A") + 27


with open(INPUT_FILE_NAME, "r") as input_file:
    lines = [line.strip() for line in input_file]

assert len(lines) % 3 == 0

for i in range(len(lines) // 3):
    s = set(lines[i * 3])
    s = s.intersection(set(lines[i * 3 + 1]))
    s = s.intersection(set(lines[i * 3 + 2]))
    assert len(s) == 1
    badge = s.pop()
    pri = get_priority(badge)

    S += pri

print(S)
