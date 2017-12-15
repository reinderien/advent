#!/usr/bin/env python3

import re


def run(lines):
    direct = {}

    def parse():
        rex = re.compile(r'\d+')
        for line in lines:
            ids = tuple(int(i) for i in rex.findall(line))
            for i, j in zip(ids[0:], ids[1:]):
                direct.setdefault(i, set()).add(j)
                direct.setdefault(j, set()).add(i)

    def count():
        visited, pending = set(), {0}
        while pending:
            current = pending.pop()
            visited.add(current)
            pending |= direct[current] - visited
        return len(visited)

    parse()
    return count()


test_input = '''0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5'''.split('\n')
assert(run(test_input) == 6)  # works

with open('12.in') as f:
    print('Part 1:', run(f))  # 141
