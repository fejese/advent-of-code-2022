#!/usr/bin/env python3

from dataclasses import dataclass


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


@dataclass
class Range:
    start: int
    end: int

    @staticmethod
    def from_str(s: str) -> "Range":
        parts = s.split("-")
        return Range(int(parts[0]), int(parts[1]))

    def overlap(self, other: "Range") -> bool:
        if self.start > other.end:
            return False
        if self.end < other.start:
            return False
        return True


@dataclass
class Pair:
    left: Range
    right: Range

    @staticmethod
    def from_line(line: str) -> "Pair":
        parts = line.strip().split(",")
        return Pair(
            Range.from_str(parts[0]),
            Range.from_str(parts[1]),
        )

    def has_overlap(self) -> bool:
        if self.left.overlap(self.right):
            return True
        return False


count: int = 0

with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        pair = Pair.from_line(line)
        if pair.has_overlap():
            count += 1

print(count)
