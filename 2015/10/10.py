#!/usr/bin/env python3

from timeit import timeit

N = 40  # 329356
# N = 50  # 4666278

def p():
    inputs = '3113322113'
    for n in range(N):
        prev, out, run = inputs[0], '', 1
        for i in inputs[1:]:
            if i == prev: run += 1
            else:
                out += '%d%c' % (run, prev)
                run, prev = 1, i
        inputs = '%s%d%c' % (out, run, prev)
    print(len(inputs))

print('t=%.3f' % timeit(p, number=1))
