#!/usr/bin/env python3

from itertools import combinations

checksum1, checksum2 = 0, 0
with open('02.in') as f:
    for line in f:
        row = [int(x) for x in line.split()]
        checksum1 += max(row) - min(row)

        # The following is n^2, but  ¯\_(ツ)_/¯
        for a, b in combinations(row, 2):
            if a < b:
                a, b = b, a
            if a % b == 0:
                checksum2 += a // b

print('Part 1:', checksum1)  # 48357
print('Part 2:', checksum2)  # 351
