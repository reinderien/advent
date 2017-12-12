#!/usr/bin/env python3

"""
Read https://www.redblobgames.com/grids/hexagons/ .
Use "cube coordinates".
"""


def run(step_string):
    basis = {
        'n' : ( 0, 1,-1),
        'ne': ( 1, 0,-1),
        'se': ( 1,-1, 0),
        's' : ( 0,-1, 1),
        'sw': (-1, 0, 1),
        'nw': (-1, 1, 0)
    }

    point = [0]*3
    dist_max = 0
    for step in step_string.split(','):
        point = [p+s for p,s in zip(point, basis[step])]
        dist = max(abs(p) for p in point)
        dist_max = max(dist_max, dist)
    return dist, dist_max

assert(run('ne,ne,ne')[0] == 3)
assert(run('ne,ne,sw,sw')[0] == 0)
assert(run('ne,ne,s,s')[0] == 2)
assert(run('se,sw,se,sw,sw')[0] == 3)

with open('11.in') as f:
    real_input = f.read().rstrip()
real_end, real_max = run(real_input)
print('Part 1:', real_end)  # 796
print('Part 2:', real_max)  # 1585
