#!/usr/bin/env python3

import json

from typing import List, Optional, Union


# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


Packet = Union[int, List["Packet"]]


def is_right_order(left: Packet, right: Packet, depth: int = 0) -> Optional[bool]:
    prefix: str = "  " * depth + "-"
    print(f"{prefix} Compare {left} vs {right}")
    left_int = isinstance(left, int)
    right_int = isinstance(right, int)
    if left_int and right_int:
        if left > right:
            print(
                f"{prefix} Right side is smaller, so inputs are not in the right order"
            )
            return False
        if left < right:
            print(f"{prefix} Left side is smaller, so inputs are in the right order")
            return True
        return None

    if left_int:
        left = [left]
        print(f"{prefix} Mixed types; convert left to {left} and retry comparison")
        return is_right_order(left, right)

    if right_int:
        right = [right]
        print(f"{prefix} Mixed types; convert right to {right} and retry comparison")
        return is_right_order(left, right)

    for i in range(min(len(left), len(right))):
        sub = is_right_order(left[i], right[i], depth + 1)
        if sub is None:
            continue
        return sub

    if len(left) < len(right):
        print(f"{prefix} Left side ran out of items, so inputs are in the right order")
        return True

    if len(left) > len(right):
        print(
            f"{prefix} Right side ran out of items, so inputs are not in the right order"
        )
        return False

    return None


right_order_pair_index_sum: int = 0
with open(INPUT_FILE_NAME, "r") as input_file:
    pair_index = 1
    while True:
        maybe_left = input_file.readline()
        if not maybe_left:
            break

        print(f"== Pair {pair_index} ==")
        left: Packet = json.loads(maybe_left)
        right: Packet = json.loads(input_file.readline())

        if is_right_order(left, right):
            print(f"ok: {pair_index}")
            right_order_pair_index_sum += pair_index
        else:
            print("notok")
        print()

        # separator
        input_file.readline()
        pair_index += 1

print(right_order_pair_index_sum)
