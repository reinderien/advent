#!/usr/bin/env python3
# http://adventofcode.com/day/1

floor, basement = 0, False
for p,i in enumerate(open('1.in').read()):
    if i == '(': floor += 1
    elif i == ')': floor -= 1
    if floor < 0 and not basement:
        basement = True
        print('Basement at', p+1)  # 1795
print('Final floor is', floor)  # 74
