#!/usr/bin/env python3

from collections import defaultdict


def run(fname):
    graph = defaultdict(set)

    with open(fname) as f:
        for line in f:
            a, b = (int(n) for n in line.split('/'))
            graph[a].add(b)
            graph[b].add(a)

    best = 0

    def recurse(visited, current=0, total=0):
        visited = set(visited)
        visited.add(current)
        to_visit = graph[current] - visited
        total += current
        if not to_visit:
            nonlocal best
            best = max(best, total)
        total += current
        for next_node in to_visit:
            recurse(visited, next_node, total)

    recurse(set())
    return best

assert(run('24.test.in') == 31)
print('Part 1:', run('24.in'))  # 1281 is too low
