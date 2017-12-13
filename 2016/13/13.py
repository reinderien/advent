#!/usr/bin/env python3

from astar import AStar
from math import sqrt


def ones(x):
    n = 0
    while x:
        n += x & 1
        x >>= 1
    return n


def run(fav, goal):
    def is_wall(x, y):
        n = ones(x*(x + 3) + y*(y + 2*x + 1) + fav)
        return n & 1

    class Cubicles(AStar):
        def heuristic_cost_estimate(self, current, goal):
            x = current[0] - goal[0]
            y = current[1] - goal[1]
            return sqrt(x ** 2 + y ** 2)

        def distance_between(self, n1, n2):
            return 1

        def neighbors(self, node):
            x0, y0 = node
            neighs = tuple((x0+x, y0+y) for (x,y) in
                           ((1,0), (-1,0), (0,1), (0,-1)))
            return (n for n in neighs if not is_wall(*n))

    path = tuple(Cubicles().astar(start=(1,1), goal=goal))
    return len(path) - 1


assert(run(10, (7, 4)) == 11)
print('Part 1:', run(1362, (31, 39)))  # 82
