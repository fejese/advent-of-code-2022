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
    for line in input_file:
        line = line.strip()
        assert len(line) % 2 == 0
        left = set(line[: len(line) // 2])
        right = set(line[len(line) // 2 :])

        common = left.intersection(right)
        assert len(common) == 1
        common = common.pop()
        pri = get_priority(common)

        print(f"{line} => left: {left}, right: {right} => {common} ({pri})")
        S += pri

print(S)
