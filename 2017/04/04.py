#!/usr/bin/env python3

total_1, total_2 = 0, 0
with open('04.in') as f:
    for line in f:
        words = line.split()
        total_1 += len(words) == len(set(words))
        awords = set(''.join(sorted(w)) for w in words)
        total_2 += len(awords) == len(words)
print('Part 1:', total_1)  # 455
print('Part 2:', total_2)  # 186
