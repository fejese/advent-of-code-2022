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
        if s in ("A", "X"):
            return Shape.Rock
        if s in ("B", "Y"):
            return Shape.Paper
        if s in ("C", "Z"):
            return Shape.Scissor
        raise NotImplementedError()

    def __repr__(self) -> str:
        return self.name


def get_outcome_score(opp: Shape, own: Shape) -> int:
    if opp.value == own.value:
        return 3

    if (opp.value + 1) % 3 == own.value:
        return 6

    return 0


outcome_score: Mapping[Tuple[Shape, Shape], int] = {
    (opp, own): get_outcome_score(opp, own) for opp in Shape for own in Shape
}

print(outcome_score)

score = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        opp, own = [Shape.from_str(i) for i in line.split(" ")]
        score += own.score
        score += outcome_score[(opp, own)]

print(score)
