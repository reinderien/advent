#!/usr/bin/env python3

from re import finditer

repls = {}
with open('19.in') as f:
    while True:
        line = f.readline().rstrip()
        if line == '': break
        kv = line.split(' => ')
        repls.setdefault(kv[0], set()).add(kv[1])
    molecule = f.readline().rstrip()

results = {molecule[:match.start()] + dest + molecule[match.end():]
           for src, dests in repls.items()
           for match in finditer(src, molecule)
           for dest in dests}

print(len(results))  # 576
