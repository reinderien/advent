#!/usr/bin/env python3

from math import sqrt


def coords(i):
    """
    This uses analytical expressions for the size of interior square of the spiral and the
    coordinates of the current cell based only on the current index. The expressions are heavily
    piecewise but this piecewise behaviour can be entirely derived from min/max/abs.

    This is O(1), yaaay
    """

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


'''
Part 2: Meh. Do the slow thing
The infinite 2D space does not need to be represented in memory; only the previous and current 
edges of the spiral.
'''

edges_p, edges_c = [[1], [1], [1], [1,1]], [None]*4
i_edge = 0
while True:
    edge_c = []
    edge_p = edges_p[i_edge]
    edges_c[i_edge] = edge_c
    for p in range(1+len(edge_p)):
        total = sum(edge_p[max(0,p-1):p+2])
        if edge_c:
            total += edge_c[-1]
        edge_c.append(total)

    edges_p[i_edge] = edge_c
    i_edge = (i_edge+1) % 4
    edges_p[i_edge].insert(0, edge_c[-2])
