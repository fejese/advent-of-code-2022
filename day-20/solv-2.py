#!/usr/bin/env python3

from dataclasses import dataclass

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"
KEY: int = 811589153


class Node:
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.prev: Node
        self.next: Node

    def move(self, node_count: int) -> None:
        if self.value == 0:
            print("noop")
            return

        move_count = self.value % (node_count - 1)
        for _ in range(move_count):
            self.next = self.next.next
            self.next.prev.next = self
            self.next.prev.prev = self.prev
            self.prev.next = self.next.prev
            self.prev = self.next.prev
            self.next.prev = self

    def print_from_here(self, prefix="") -> None:
        print(f"{prefix}[{self.value}", end="")
        curr = self.next
        while curr != self:
            print(f", {curr.value}", end="")
            curr = curr.next
        print("]")


with open(INPUT_FILE_NAME, "r") as input_file:
    nodes = [Node(int(line.strip()) * KEY) for line in input_file]

for i, node in enumerate(nodes):
    prev_i = (i - 1) % len(nodes)
    next_i = (i + 1) % len(nodes)
    node.next = nodes[next_i]
    node.prev = nodes[prev_i]
    if node.value == 0:
        z_node = node

# nodes[0].print_from_here()

for round_i in range(10):
    for i, node in enumerate(nodes):
        print(f"Round {round_i} / Step {i}: moving {node.value}")
        node.move(len(nodes))
        # nodes[0].print_from_here()

curr = z_node
s = 0
for i in range(3):
    for _ in range(1000):
        curr = curr.next
    print(curr.value)
    s += curr.value
print(s)
