#!/usr/bin/env python3

import re

cardinals = ((0, 1), (-1, 0), (0, -1), (1, 0))  # NWSE
dirs = [(m.group(1), int(m.group(2)))
        for m in re.finditer(
           r'(L|R)(\d+)(\D|$)', file('01.in').read())]


def walk(part):
    facing, px, py = 0, 0, 0
    visited = set()
    for d in dirs:
        facing = (facing + (1 if d[0] == 'L' else -1)) % 4
        px += cardinals[facing][0]*d[1]
        py += cardinals[facing][1]*d[1]
        if part == 2:
            if (px, py) in visited:
                break
            visited.add((px, py))
    print(abs(px) + abs(py))

walk(1)  # 161 - correct
walk(2)  # 156 - incorrect
