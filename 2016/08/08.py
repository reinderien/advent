#!/usr/bin/env python3

import re

X, Y = 50, 6
screen = [[False for x in range(X)] for y in range(Y)]

pat_rect = re.compile(r'^(rect) (\d+)x(\d+)$')
pat_rotate_row = re.compile(r'^(rotate row) y=(\d+) by (\d+)$')
pat_rotate_col = re.compile(r'^(rotate column) x=(\d+) by (\d+)$')

for line in open('08.in'):
    m = (pat_rect.match(line) or
         pat_rotate_row.match(line) or
         pat_rotate_col.match(line))
    cmd, a, b = m.groups()
    a, b = int(a), int(b)

    if cmd == 'rect':
        for y in range(b):
            screen[y][:a] = [True]*a
    elif cmd == 'rotate row':
        screen[a] = screen[a][-b:] + screen[a][:-b]
    elif cmd == 'rotate column':
        col = [screen[y][a] for y in range(Y)]
        col = col[-b:] + col[:-b]
        for y in range(Y):
            screen[y][a] = col[y]


pels = sum(p for row in screen for p in row)
print(pels)
# 106 is correct
