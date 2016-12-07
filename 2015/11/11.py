#!/usr/bin/env python3

import re

# cqjxjnds for p1, producing cqjxxyzz
# cqjxxyzz for p2, producing cqkaabcc
orig = 'cqjxxyzz'
digits, x = 'abcdefghjkmnpqrstuvwxyz', 0
radix, pairs = len(digits), re.compile(r'([a-z])\1.*([a-z])\2')
for d in orig: x = x*radix + digits.index(d)

while True:
    x += 1
    xc, current = x, ''
    while xc:
        xc, d = divmod(xc, radix)
        current = digits[d] + current

    if not pairs.search(current): continue
    for start in range(len(current) - 2):
        straight = current[start:start+3]
        if ord(straight[0]) == ord(straight[1])-1 == ord(straight[2])-2:
            print(current)
            exit()
