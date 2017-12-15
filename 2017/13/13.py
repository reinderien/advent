#!/usr/bin/env python3


def run(fname):
    with open(fname) as f:
        layers = tuple(tuple(int(i) for i in l.rstrip().split(': '))
                       for l in f)
    return


assert(run('13.test.in') == 24)
print('Part 1:', run('13.in'))
