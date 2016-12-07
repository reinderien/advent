#!/usr/bin/env python3

from re import findall
from json import load

# lol
# 156366
print(sum(int(s) for l in open('12.in').readlines() for s in findall('[-\d]+',l)))

# ok really this time
with open('12.in') as f:
    doc = load(f)

def recurse(node):
    if type(node) is int: return node
    if type(node) is dict:
        if 'red' in node.values(): return 0
        values = node.values()
    elif type(node) is list: values = node
    else: return 0
    return sum(recurse(n) for n in values)

# 96852
print(recurse(doc))
