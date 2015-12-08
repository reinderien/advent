#!/usr/bin/env python3
# http://adventofcode.com/day/2

paper, ribbon = 0,0
for line in open('2.in').readlines():
    a,b,c = tuple(sorted(int(d) for d in line.strip().split('x')))
    paper += 3*a*b + 2*c*(a + b)
    ribbon += 2*(a+b) + a*b*c
print('Paper:', paper)  # 1598415
print('Ribbon:', ribbon)  # 3812909
