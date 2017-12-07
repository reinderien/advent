#!/usr/bin/env python3

total = 0
with open('04.in') as f:
    for line in f:
        words = line.split()
        total += len(words) == len(set(words))
print('Part 1:', total)  # 455

