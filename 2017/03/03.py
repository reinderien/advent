#!/usr/bin/env python3

from math import sqrt


def coords(i):
    """
    This uses analytical expressions for the size of interior square of the spiral and the
    coordinates of the current cell based only on the current index. The expressions are heavily
    piecewise but this piecewise behaviour can be entirely derived from min/max/abs.

    This is O(1), yaaay
    """

    # Edge case

    w = ((sqrt(i-1)-1)//2)*2 + 1  # Width of inner square
    edge = (w+1)//2               # Max displacement from centre
    x = abs(w**2 + 2.5*w + 2.5 - i) - w - 1
    y = w + 1 - abs(w**2 + 1.5*w + 1.5 - i)
    x = min(edge, max(-edge, x))
    y = min(edge, max(-edge, y))
    return int(x), int(y)


def taxi(x, y):
    return abs(x) + abs(y)

assert(taxi(*coords(1)) == 0)
assert(taxi(*coords(12)) == 3)
assert(taxi(*coords(23)) == 2)
assert(taxi(*coords(1024)) == 31)

i = 325489
c = coords(i)
d = taxi(*c)  # 552
print('Part 1:')
print('i=%d x,y=(%d,%d) d=%d' % (i, *c, d))


