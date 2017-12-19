#!/usr/bin/env python3

from itertools import chain


def run(fname):
    with open(fname) as f:
        lines = tuple(f)

    deltas = ((0, 1), ( 1,0),
              (0,-1), (-1,0))
    old_dir_i = 0
    coord = (lines[0].find('|'), 0)
    found = ''

    while True:
        xo, yo = coord
        dirs = ((i+old_dir_i)%4 for i in (0,1,3))
        for dir_i in dirs:
            dirn = deltas[dir_i]
            x, y = xo + dirn[0], yo + dirn[1]
            c = lines[y][x]
            if c != ' ':
                break
        else:
            return found
        old_dir_i = dir_i
        coord = x,y
        if c.isalpha():
            found += c


assert(run('19.test.in') == 'ABCDEF')
print('Part 1:', run('19.in'))
