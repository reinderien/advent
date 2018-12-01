#!/usr/bin/env python3

from collections import namedtuple
import re


Node = namedtuple('Node', ('x', 'y', 'size', 'used', 'avail', 'use'))


def parse():
    line_re = re.compile(r'^/dev/grid/node-x(\d+)-y(\d+) +'
                         r'(\d+)T +'
                         r'(\d+)T +'
                         r'(\d+)T +'
                         r'(\d+)%$')

    with open('input.txt') as f:
        for line in f:
            m = line_re.match(line.rstrip())
            if not m:
                continue
            yield Node(*(int(i) for i in m.groups()))


def p1():
    nodes = list(parse())
    # data on A fits on B
    nodes.sort(key=lambda n: n.avail)

    total = 0
    to_idx = 0
    for from_idx in range(len(nodes) - 1):
        while nodes[from_idx].used > nodes[to_idx].avail and \
         from_idx < len(nodes)-1:
            from_idx += 1

        total += len(nodes) - to_idx + 1

    return total


print(p1())  # 1102499 is too high
