#!/usr/bin/env python3

valid = 0
for line in open('03.in'):
    sides = tuple(sorted(int(i) for i in line.split()))
    if sides[2] < sides[0] + sides[1]:
        valid += 1

print(valid)  # 1050 - correct


valid = 0
end = False
with open('03.in') as f:
    while True:
        triangles = [[], [], []]
        for _ in range(3):
            line = f.readline().strip()
            if not line:
                end = True
                break
            sides = tuple(int(i) for i in line.split())
            for triangle, side in zip(triangles, sides):
                triangle += (side,)
        if end: break
        for triangle in triangles:
            sides = tuple(sorted(triangle))
            if sides[2] < sides[0] + sides[1]:
                valid += 1

print(valid)
