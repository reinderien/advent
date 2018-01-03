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


def recurse_p2(graph, visited, left=0, depth=0):
    next_pairs = {(left, right) for right in graph[left]} - visited
    if not next_pairs:
        return depth, 0
    best_depth, total, right = max((*recurse_p2(graph, visited | {pair, pair[::-1]},
                                                pair[1], depth+1), pair[1])
                                   for pair in next_pairs)
    return best_depth, total + left + right


def p1(graph):
    return recurse_p1(graph, set())


def p2(graph):
    return recurse_p2(graph, set())

test_graph = parse('24.test.in')
assert(p1(test_graph) == 31)
assert(p2(test_graph) == (4, 19))

real_graph = parse('24.in')
print('Part 1:', p1(real_graph))  # 1859
print('Part 2: depth=%d strength=%d' % p2(real_graph))  # depth=35 strength=1799
