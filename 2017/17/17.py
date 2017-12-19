#!/usr/bin/env python3


def p1(pitch):  # naive impl
    seq = [0]
    pos = 0
    for value in range(1, 2018):
        pos = (pos + pitch + 1) % len(seq)
        seq.insert(pos+1, value)
    return seq[(pos + 2) % len(seq)]

assert(p1(3) == 638)
print('Part 1:', p1(369))  # 1547
