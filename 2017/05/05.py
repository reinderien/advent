#!/usr/bin/env python3


def run(offsets, first):
    steps, index = 0, 0
    while True:
        offset = offsets[index]
        if offset >= 3 and not first:
            offsets[index] -= 1
        else:
            offsets[index] += 1
        index += offset
        steps += 1
        if not (0 <= index < len(offsets)):
            return steps

assert(run([0, 3, 0, 1, -3], first=True) == 5)
assert(run([0, 3, 0, 1, -3], first=False) == 10)

with open('05.in') as f:
    file_offsets = [int(line) for line in f]
print('Part 1:', run(file_offsets, first=True))   # 376976
print('Part 2:', run(file_offsets, first=False))  # 739 (wrong)
