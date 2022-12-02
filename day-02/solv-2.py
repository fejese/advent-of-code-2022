#!/usr/bin/env python3

from enum import Enum
from typing import Mapping, Tuple

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


class Shape(Enum):
    Rock = 0
    Paper = 1
    Scissor = 2

    @property
    def score(self) -> int:
        return self.value + 1

    @staticmethod
    def from_str(s: str) -> "Shape":
        s = s.strip()
        if s == "A":
            return Shape.Rock
        if s == "B":
            return Shape.Paper
        if s == "C":
            return Shape.Scissor
        raise NotImplementedError()

    def __repr__(self) -> str:
        return self.name


class Outcome(Enum):
    Lose = 0
    Draw = 3
    Win = 6

    @staticmethod
    def from_str(s: str) -> "Outcome":
        s = s.strip()
        if s == "X":
            return Outcome.Lose
        if s == "Y":
            return Outcome.Draw
        if s == "Z":
            return Outcome.Win
        raise NotImplementedError()

    def __repr__(self) -> str:
        return self.name


def get_own_shape(opp: Shape, outcome: Outcome) -> Shape:
    diff = outcome.value // 3 - 1
    return Shape((opp.value + diff) % 3)


score = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        parts = line.split(" ")
        opp = Shape.from_str(parts[0])
        outcome = Outcome.from_str(parts[1])
        score += outcome.value
        score += get_own_shape(opp, outcome).score

print(score)
