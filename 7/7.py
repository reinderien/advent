#!/usr/bin/env python3
# http://adventofcode.com/day/7

from collections import namedtuple

Gate = namedtuple('Gate', ('op', 'a', 'b'))

gates = {}
for line in open('7.in').readlines():
    parts = line.strip().split(' ')
    if len(parts) == 3:
        op, b, (a, _, out) = 'EQ', None, parts
    elif len(parts) == 4:
        b, (op, a, _, out) = None, parts
    elif len(parts) == 5:
        a, op, b, _, out = parts
    else:
        raise ValueError()

    try:
        if a is not None: a = int(a)
    except ValueError:
        pass
    try:
        if b is not None: b = int(b)
    except ValueError:
        pass

    gates[out] = Gate(op, a, b)
orig_gates = dict(gates)

ops = {'EQ': lambda a, b: a,
       'NOT': lambda a, b: ~a,
       'AND': lambda a, b: a & b,
       'OR': lambda a, b: a | b,
       'LSHIFT': lambda a, b: a << b,
       'RSHIFT': lambda a, b: a >> b}


def recurse(out):
    gate = gates[out]
    a, b, op = gate.a, gate.b, ops[gate.op]
    if type(a) is str: a = recurse(a)
    if type(b) is str: b = recurse(b)
    val = op(a, b)
    gates[out] = Gate('EQ', val, None)
    return val


a_val = recurse('a')
print(a_val)  # 16076

gates = orig_gates
gates['b'] = Gate('EQ', a_val, None)
print(recurse('a'))  # 2797
