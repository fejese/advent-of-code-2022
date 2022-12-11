#!/usr/bin/env python3

from typing import Callable, List

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

ROUNDS: int = 20


class Monkey:
    def __init__(self) -> None:
        self.items: List[int]
        self.operation: Callable[[int], int]
        self.test: Callable[[int], bool]
        self.next_true: int
        self.next_false: int
        self.inspections: int = 0

    def __repr__(self) -> str:
        return (
            f"[{self.items}, {self.next_true}, {self.next_false}, {self.inspections}]"
        )


def get_operation(line: str) -> Callable[[int], int]:
    parts = line.split("=")

    def func(old: int) -> int:
        return eval(parts[1].strip())

    return func


def get_test(line: str) -> Callable[[int], bool]:
    c = int(line.split(" ")[-1])

    def func(n: int) -> bool:
        return n % c == 0

    return func


def print_monkeys() -> None:
    global monkeys
    for mi, m in enumerate(monkeys):
        print(f"Monkey {mi}: {m.items}, {m.inspections}")
    print()


monkeys: List[Monkey] = []


with open(INPUT_FILE_NAME, "r") as input_file:
    monkey_defs = [
        [line.split(":")[-1].strip() for line in mdef.splitlines()[1:]]
        for mdef in input_file.read().split("\n\n")
    ]
    for mdef in monkey_defs:
        monkey = Monkey()
        monkey.items = [int(i) for i in mdef[0].split(", ")]
        monkey.operation = get_operation(mdef[1])
        monkey.test = get_test(mdef[2])
        monkey.next_true = int(mdef[3].split(" ")[-1])
        monkey.next_false = int(mdef[4].split(" ")[-1])
        monkeys.append(monkey)

print(monkey_defs)
print_monkeys()

for _ in range(ROUNDS):
    for mi, active_monkey in enumerate(monkeys):
        for item in active_monkey.items:
            item = active_monkey.operation(item) // 3
            target_mi = (
                active_monkey.next_true
                if active_monkey.test(item)
                else active_monkey.next_false
            )
            monkeys[target_mi].items.append(item)
            active_monkey.inspections += 1
        monkeys[mi].items = []
    print_monkeys()


top_inspections = sorted([m.inspections for m in monkeys], reverse=True)[:2]
print(top_inspections[0] * top_inspections[1])
