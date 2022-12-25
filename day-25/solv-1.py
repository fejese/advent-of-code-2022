#!/usr/bin/env python3

from typing import Dict, Optional

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

ENC_MAP: Dict[int, str] = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}
DEC_MAP: Dict[str, int] = {v: k for k, v in ENC_MAP.items()}


total = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        base = 1
        num = 0
        for ch in reversed(line.strip()):
            num += base * DEC_MAP[ch]
            base *= 5

        total += num


print(total)


def calc(target: int, pow: int = 21) -> Optional[str]:
    # print(f"pow: {pow:2} target: {target:20}")
    diff_max = 0
    for i in range(0, pow):
        diff_max += 2 * 5**i
    # print(f"  diff_max: {diff_max:24}")
    for i in (-2, -1, 0, 1, 2):
        curr = i * 5**pow
        curr_ch = ENC_MAP[i]
        # print(f"  curr:     {curr:24}")
        if curr == target:
            return curr_ch + "0" * (pow)
        diff = target - curr
        # print(f"  diff:     {curr:24}")
        if abs(diff) > diff_max:
            continue
        sub = calc(diff, pow - 1)
        if sub is not None:
            return curr_ch + sub
    return None


print(calc(total).lstrip("0"))
