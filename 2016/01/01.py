#!/usr/bin/env python3

import re

cardinals = ((0, 1), (-1, 0), (0, -1), (1, 0))  # NWSE
dirs = [(m.group(1), int(m.group(2)))
        for m in re.finditer(
           r'(L|R)(\d+)(\D|$)', open('01.in').read())]


def walk(part):
    facing, px, py = 0, 0, 0
    visited = set()
    for d in dirs:
        facing = (facing + (1 if d[0] == 'L' else -1)) % 4
        ux, uy = cardinals[facing][0], cardinals[facing][1]
        if part == 1:
            px += ux*d[1]
            py += uy*d[1]
        else:
            # The fancy thing to do is store line endpoints, but let's be bad
            for _ in range(d[1]):
                px += ux
                py += uy
                if (px, py) in visited:
                    break
                visited.add((px, py))
            else:
                continue
            break
    print(abs(px) + abs(py))

walk(1)  # 161 - correct
walk(2)  # 110 - correct
