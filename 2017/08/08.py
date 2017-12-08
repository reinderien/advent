#!/usr/bin/env python3

import operator
from sys import maxsize


def run(lines):
    regs = {}
    ops = {'inc': operator.add, 'dec': operator.sub,
           '<': operator.lt, '>': operator.gt,
           '<=': operator.le, '>=': operator.ge,
           '==': operator.eq, '!=': operator.ne}
    highest = -maxsize
    for line in lines:
        opl, op, opr, _, compl, comp, compr = line.split()
        if ops[comp](regs.get(compl,0), int(compr)):
            newreg = ops[op](regs.get(opl,0), int(opr))
            regs[opl] = newreg
            highest = max(highest, newreg)
    return regs, highest


def p1(lines):
    return max(lines.values())

test_lines = \
'''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''.split('\n')
test_regs, test_highest = run(test_lines)
assert(p1(test_regs) == 1)
assert(test_highest == 10)

with open('08.in') as f:
    file_regs, file_highest = run(f)
    print('Part 1:', p1(file_regs))  # 8022
    print('Part 2:', file_highest)
