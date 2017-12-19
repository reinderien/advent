#!/usr/bin/env python3


def p1(pitch):  # naive impl
    seq = [0]
    pos = 0
    for value in range(1, 2018):
        pos = (pos + pitch + 1) % len(seq)
        seq.insert(pos+1, value)
    return seq[(pos + 2) % len(seq)]


def p2():
    """
    It's a circular buffer, so when an insertion occurs at n, does it actually go on the end or
    does it get inserted before the beginning? Always the end. This in turn means that element 0
    will always be first, and we don't need to track any of the list contents.
    """
    pos, second = 0, None
    for value in range(50_000_001):
        if not pos:
            second = value
        pos = (pos + 369 + 1) % (value + 1)
    return second

assert(p1(3) == 638)
print('Part 1:', p1(369))  # 1547
print('Part 2:', p2())     # 31154878, slow
