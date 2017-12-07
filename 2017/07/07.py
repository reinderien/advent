#!/usr/bin/env python3

from collections import namedtuple
import re

Node = namedtuple('Node', ('name', 'weight', 'children'))


def parse_tree(raw):
    parse = re.compile(r'^(?P<name>\S+) '
                       r'\((?P<weight>\d+)\)'
                       r'( -> '
                       r'(?P<children>.+)'
                       r')?$')
    tree = {}
    nodes = []
    for line in raw:
        match = parse.match(line)
        if not match:
            continue

        children = match.group('children')
        if children:
            children = {name: None for name in children.split(', ')}
        else:
            children = {}

        node = Node(name=match.group('name'),
                    weight=int(match.group('weight')),
                    children=children)
        tree[node.name] = node
        nodes.append(node)

    for node in nodes:
        for child_name in node.children.keys():
            node.children[child_name] = tree[child_name]
            tree.pop(child_name)

    return tree


def top(t):
    return tuple(t.keys())

test_input = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''.split('\n')
test_tree = parse_tree(test_input)

with open('07.in') as f:
    file_tree = parse_tree(f)

assert(top(test_tree) == ('tknk',))
print('Part 1:', top(file_tree))  # mwzaxaj
