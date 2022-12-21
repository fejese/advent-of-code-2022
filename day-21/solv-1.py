#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def calc(data, key):
    expr = data[key]
    if isinstance(expr, int):
        return expr

    left = calc(data, expr[0])
    right = calc(data, expr[2])
    if expr[1] == "/":
        value = left // right
    elif expr[1] == "*":
        value = left * right
    elif expr[1] == "+":
        value = left + right
    elif expr[1] == "-":
        value = left - right
    else:
        raise Exception(f"wat: {key} => {expr}")

    data[key] = value
    return value


data = {}
with open(INPUT_FILE_NAME, "r") as input_file:
    for line in input_file:
        key, rest = line.strip().split(": ")
        if rest.isnumeric():
            data[key] = int(rest)
        else:
            data[key] = rest.split(" ")


print(calc(data, "root"))
