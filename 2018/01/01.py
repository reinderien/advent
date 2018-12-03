#!/usr/bin/env python3

from itertools import cycle

print('Part 1:')
with open('input.txt') as f:
    print(sum(int(l) for l in f))  # 582

print('Part 2:')
seen = set()
freq = 0
with open('input.txt') as f:
    freqs = tuple(int(l) for l in f)
for l in cycle(freqs):
    if freq in seen:
        break
    seen.add(freq)
    freq += int(l)
print(freq)
