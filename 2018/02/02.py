#!/usr/bin/env python3

from collections import Counter


def p1(fname):
    dupes_2, dupes_3 = 0,0
    with open(fname) as f:
        for line in f:
            count = Counter(line)
            dupes_2 += int(2 in count.values())
            dupes_3 += int(3 in count.values())
    return dupes_2 * dupes_3


print('Part 1:')
assert(p1('test_input.txt') == 12)
print(p1('input.txt'))
