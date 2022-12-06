#!/usr/bin/env python3

# INPUT_FILE_NAME: str = "test-input"
INPUT_FILE_NAME: str = "input"

with open(INPUT_FILE_NAME, "r") as input_file:
    buffer = []
    pos = 1
    while True:
        next_char = input_file.read(1)
        if not next_char:
            break
        buffer.append(next_char)
        # print(pos, buffer)
        if len(set(buffer)) == 14:
            print(pos)
            input_file.readline()
            buffer = []
            pos = 1
            continue
        pos += 1
        if len(buffer) >= 14:
            buffer = buffer[1:]
