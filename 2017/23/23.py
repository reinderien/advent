#!/usr/bin/env python3


def run(p2=False):
    n_mul, ip = 0, 0
    regs = [0]*8
    if p2:
        regs[0] = 1

    def fetch(i):
        try:
            i = int(i)
            return lambda: i
        except ValueError:
            i = ord(i) - ord('a')
            return lambda: regs[i]

    def op_set(x, y):
        regs[x] = y()

    def op_sub(x, y):
        regs[x] -= y()

    def op_mul(x, y):
        regs[x] *= y()
        nonlocal n_mul
        n_mul += 1

    def op_jnz(x, y):
        if x() != 0:
            nonlocal ip
            ip += y() - 1

    ops = {'set': op_set,
           'sub': op_sub,
           'mul': op_mul,
           'jnz': op_jnz}

    def parse(line):
        op, x, y = line.rstrip().split(' ')
        y = fetch(y)
        if op == 'jnz':
            x = fetch(x)
        else:
            x = ord(x) - ord('a')
        fun = ops[op]
        return lambda: fun(x, y)

    with open('23.in') as f:
        prog = tuple(parse(l) for l in f)

    while 0 <= ip < len(prog):
        prog[ip]()
        ip += 1

    if p2:
        return regs[-1]
    return n_mul

print('Part 1:', run(p2=False))  # 4225
# print('Part 2:', run(p2=True)) # don't do this, it's too slow
