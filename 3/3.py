#!/usr/bin/env python3

houses = {(0,0)}
deltas = {'>': (1,0), '<': (-1,0), '^': (0,1), 'v': (0,-1)}
inputs = iter(open('3.in').read())

def p1():
    x,y = 0,0
    for i in inputs:
        d = deltas[i]
        x += d[0]
        y += d[1]
        houses.add((x,y))

def p2():
    sx,sy,rx,ry = 0,0,0,0
    try:
        while True:
            ds, dr = deltas[next(inputs)], deltas[next(inputs)]
            sx += ds[0]
            sy += ds[1]
            rx += dr[0]
            ry += dr[1]
            houses.add((sx,sy))
            houses.add((rx,ry))
    except StopIteration: pass

p1()  # 2565
#p2()  # 2639
print(len(houses))
