#!/usr/bin/env python3

def p(N):
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

p(40)  # 329356
p(50)  # 4666278
