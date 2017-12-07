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


def check_tree(tree):
    if not tree:
        return 0
    weights = tuple((node.weight + check_tree(node.children), node)
                     for node in tree.values())
    weight_qs = tuple(w[0] for w in weights)
    all_weights = set(weight_qs)
    if len(all_weights) != 1:
        weight_counts = tuple(sorted((sum(1 for wc in weights if w==wc[0]), w)
                                     for w in all_weights))
        bad_weight = weight_counts[0][1]
        others_weight = weight_counts[1][1]
        bad_node = next(w[1] for w in weights if w[0] == bad_weight)

        print('Bad node found.')
        print('                     Name:', bad_node.name)
        print('Neighbour combined weight:', others_weight)
        print('      Own combined weight:', bad_weight)
        print('               Own weight:', bad_node.weight)
        print('    Own weight to balance:', others_weight - bad_weight + bad_node.weight)
        raise EOFError()
    return sum(weight_qs)

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
print()

print('Part 2 test:')
try:
    check_tree(test_tree)
except EOFError:
    pass
'''
                     Name: ugml
Neighbour combined weight: 243
      Own combined weight: 251
               Own weight: 68
    Own weight to balance: 60
'''

print()
print('Part 2:')
try:
    check_tree(file_tree)
except EOFError:
    pass
'''
                     Name: vrgxe
Neighbour combined weight: 2159
      Own combined weight: 2166
               Own weight: 1226
    Own weight to balance: 1219
'''
