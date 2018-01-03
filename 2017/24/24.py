#!/usr/bin/env python3

from collections import defaultdict


def run(fname):
    graph = defaultdict(set)

    with open(fname) as f:
        for line in f:
            a, b = (int(n) for n in line.split('/'))
            graph[a].add(b)
            graph[b].add(a)

    def recurse(visited, current=0):
        visited = set(visited)
        visited.add(current)
        to_visit = graph[current] - visited
        if not to_visit:
            return current
        return 2*current + max(recurse(visited, next_node)
                               for next_node in to_visit)
    return recurse(set())

assert(run('24.test.in') == 31)
print('Part 1:', run('24.in'))  # 1281 is too low
