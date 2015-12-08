#!/usr/bin/env python3

from re import sub

lines = [line.strip() for line in open('8.in').readlines()]

total = sum(len(line.strip()) - len(eval(line))
            for line in lines)
print(total)  # 1350

def escape(match):
    c = match.group()
    if c == '\\': return '\\\\'
    if c == '"': return '\\"'

total = 0
for line in lines:
    new = '"' + sub(r'\\|"', escape, line) + '"'
    total += len(new) - len(line)
print(total)  # 2085