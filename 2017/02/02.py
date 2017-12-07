#!/usr/bin/env python3

from itertools import combinations


def fin():
    with open('02.in') as f:
        for line in f:
            yield [int(x) for x in line.split()]

checksum = 0
for row in fin():
    checksum += max(row) - min(row)
print('Part 1:', checksum)  # 48357

# The following is n^2, but  ¯\_(ツ)_/¯

checksum = 0
for row in fin():
    for a, b in combinations(row, 2):
        if a < b:
            a, b = b, a
        if a % b == 0:
            checksum += a // b
print('Part 2:', checksum)  # 351
