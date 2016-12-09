#!/usr/bin/env python3

import re


abba = re.compile(r'([^\[\]])([^\[\]])(?!\1)\2\1')
hyper = re.compile(r'\[[^\[\]]*([^\[\]])([^\[\]])(?!\1)\2\1[^\[\]]*\]')

def valid(ip):
    return (
        abba.search(ip)
        and not hyper.search(ip))

# Tests from question
assert(valid('abba[mnop]qrst'))
assert(not valid('abcd[bddb]xyyx'))
assert(not valid('aaaa[qwer]tyui'))
assert(valid('ioxxoj[asdfgh]zxcvbn'))

# Addl tests
assert(valid('ioxxoj[abbbbe]zxcvbn'))

nvalid = sum(1 for line in open('07.in') if valid(line))
print(nvalid)
