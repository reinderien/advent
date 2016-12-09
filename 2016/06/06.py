#!/usr/bin/env python3

from collections import Counter

freqs = None

for line in open('06.in'):
    if freqs is None:
        freqs = [Counter() for _ in line]
    for i, c in enumerate(line):
        freqs[i][c] += 1

msg = ''.join(f.most_common(1)[0][0] for f in freqs)
print(msg)  # qrqlznrl - Correct

