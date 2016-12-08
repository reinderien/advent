#!/usr/bin/env python3

dirs = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}
digits = ('123',
          '456',
          '789')

for line in open('02.in'):
    x, y = 1, 1
    for c in line.strip():
        dx, dy = dirs[c]
        x, y = max(0, min(2, x+dx)), max(0, min(2, y+dy))
    print(digits[y][x], end='')
print()

# 38961 - correct
