#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"


def calc(data, key, humn_val):
    if key == "humn":
        return humn_val

    expr = data[key]
    if isinstance(expr, int):
        return expr

    left = calc(data, expr[0], humn_val)
    right = calc(data, expr[2], humn_val)
    if isinstance(left, int) and isinstance(right, int):
        if expr[1] == "/":
            value = left // right
        elif expr[1] == "*":
            value = left * right
        elif expr[1] == "+":
            value = left + right
        elif expr[1] == "-":
            value = left - right
        elif expr[1] == "==":
            print(left, right)
            value = left == right
        else:
            raise Exception(f"wat: {key} => {expr}")
    else:
        expr[0] = left
        expr[2] = right
        value = expr
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
            if key == "root":
                data[key][1] = "=="

left, eq, right = calc(data, "root", "X")
if isinstance(left, int):
    num = left
    expr = right
else:
    num = right
    expr = left

print(expr, num)


while "X" != expr:
    left, op, right = expr
    if isinstance(left, int):
        tmp_num = left
        expr = right
    else:
        tmp_num = right
        expr = left
    if op == "+":
        num -= tmp_num
    elif op == "*":
        num //= tmp_num
    elif op == "-":
        if tmp_num == right:
            num += tmp_num
        else:
            num = tmp_num - num
    elif op == "/":
        if tmp_num == right:
            num *= tmp_num
        else:
            num = tmp_num / num

    print(expr, num)
