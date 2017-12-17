#!/usr/bin/env python3


def count(off):
    return sum(x for i, x in enumerate(digits)
               if x == digits[(i + off) % len(digits)])

with open('01.in') as f:
    digits = [int(c) for c in f.read()]
print('Part 1:', count(1))  # 1150
print('Part 2:', count(len(digits)//2))  # 1064
