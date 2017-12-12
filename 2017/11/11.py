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
    for step in step_string.split(','):
        point = [p+s for p,s in zip(point, basis[step])]

    return max(abs(p) for p in point)

assert(run('ne,ne,ne') == 3)
assert(run('ne,ne,sw,sw') == 0)
assert(run('ne,ne,s,s') == 2)
assert(run('se,sw,se,sw,sw') == 3)

with open('11.in') as f:
    real_input = f.read().rstrip()
print('Part 1:', run(real_input))  # 796
