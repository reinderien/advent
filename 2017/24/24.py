#!/usr/bin/env python3

from collections import defaultdict


def run(fname):
    # Lines ("parts") are unique regardless of orientation.
    graph = defaultdict(set)
    with open(fname) as f:
        for line in f:
            a, b = (int(n) for n in line.split('/'))
            graph[a].add(b)
            graph[b].add(a)

    def recurse(visited, left=0):
        next_pairs = {(left, right) for right in graph[left]} - visited
        if not next_pairs:
            return 0
        return left + max(pair[1] + recurse(visited | {pair, pair[::-1]}, pair[1])
                          for pair in next_pairs)
    return recurse(set())

assert(run('24.test.in') == 31)
print('Part 1:', run('24.in'))  # 1859
