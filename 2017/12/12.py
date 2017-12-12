#!/usr/bin/env python3

import re
from itertools import combinations


def run(lines):
    groups = {}

    def assoc(i, j):
        i_group, j_group = groups.get(i), groups.get(j)
        if i_group is None and j_group is None:
            group = {i, j}
            groups[i] = group
            groups[j] = group
        elif i_group is not None and j_group is None:
            i_group.add(j)
            groups[j] = i_group
        elif j_group is not None and i_group is None:
            j_group.add(i)
            groups[i] = j_group
        elif i_group is not None and j_group is not None:
            i_group |= j_group
            groups[j] = i_group

    def parse():
        rex = re.compile(r'\d+')
        for line in lines:
            ids = tuple(int(i) for i in rex.findall(line))
            for i1, i2 in combinations(ids, 2):
                assoc(i1, i2)
            # assoc(ids[0], ids[-1])

    parse()

    return len(groups[0])


test_input = '''0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5'''.split('\n')
assert(run(test_input) == 6)  # works

'''
21 is wrong
4 is wrong
'''
with open('12.in') as f:
    print('Part 1:', run(f))
