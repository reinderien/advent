#!/usr/bin/env python3

from re import findall, search

def p1(line):
    return (len(findall(r'[aeiou]', line)) >= 3 and
            search(r'([a-z])\1', line) and
            not search(r'ab|cd|pq|xy', line))
def p2(line):
    return (search(r'([a-z]{2}).*\1', line) and
            search(r'([a-z])[a-z]\1', line))

# 258, 53
print(sum(1 for line in open('5.in').readlines() if p2(line)))
