#!/usr/bin/env python3


def run(offsets, first):
    steps, index = 0, 0
    offsets = list(offsets)
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

example = (0, 3, 0, 1, -3)
assert(run(example, first=True) == 5)
assert(run(example, first=False) == 10)

with open('05.in') as f:
    file_offsets = tuple(int(line) for line in f)
print('Part 1:', run(file_offsets, first=True))   # 376976

# See C impl
# print('Part 2:', run(file_offsets, first=False))  # 29227751 (slow)
