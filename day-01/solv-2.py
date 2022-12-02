#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    input = input_file.read()
    input_per_elf = input.split("\n\n")
    sum_per_elf = [
        sum(int(cal) for cal in input.split("\n") if cal) for input in input_per_elf
    ]

sum_per_elf = sorted(sum_per_elf, reverse=True)
print(sum(sum_per_elf[:3]))
