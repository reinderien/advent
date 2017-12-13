#!/usr/bin/env python3

from astar import AStar
from math import sqrt


def ones(x):
    n = 0
    while x:
        n += x & 1
        x >>= 1
    return n


def run(fav, goal=None):
    def is_wall(x, y):
        if x<0 or y<0: return True
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
            x, y = node
            neighs = tuple((x+a, y+b) for a,b in
                           ((1,0), (-1,0), (0,1), (0,-1)))
            return (n for n in neighs if not is_wall(*n))

    cubes = Cubicles()
    if goal:
        path = tuple(cubes.astar(start=(1,1), goal=goal))
        return len(path) - 1

    n_locs = 0
    for gy in range(52):
        for gx in range(int(sqrt(52**2 - gy**2))):
            if is_wall(gx, gy):
                continue
            path = cubes.astar(start=(1,1), goal=(gx,gy))
            if path is not None and len(tuple(path))-1 <= 50:
                n_locs += 1
    return n_locs


assert(run(10, (7, 4)) == 11)
real_fav, real_goal = 1362, (31, 39)
print('Part 1:', run(real_fav, real_goal))  # 82
print('Part 2:', run(real_fav))  # 138 (slow)
