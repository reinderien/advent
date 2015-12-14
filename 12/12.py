#!/usr/bin/env python3

from re import findall

# lol
print(sum(int(s) for l in open('12.in').readlines() for s in findall('[-\d]+',l)))

# ok really this time
