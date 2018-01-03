#!/usr/bin/env python3

from collections import defaultdict


def parse(fname):
    # Lines ("parts") are unique regardless of orientation.
    graph = defaultdict(set)
    with open(fname) as f:
        for line in f:
            a, b = (int(n) for n in line.split('/'))
            graph[a].add(b)
            graph[b].add(a)
    return graph


def recurse_p1(graph, visited, left=0):
    next_pairs = {(left, right) for right in graph[left]} - visited
    if not next_pairs:
        return 0
    return left + max(pair[1] + recurse_p1(graph, visited | {pair, pair[::-1]}, pair[1])
                      for pair in next_pairs)


def p1(graph):
    return recurse_p1(graph, set())

test_graph = parse('24.test.in')
assert(p1(test_graph) == 31)

real_graph = parse('24.in')
print('Part 1:', p1(real_graph))  # 1859
