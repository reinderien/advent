#!/usr/bin/env python3


n_mul, ip = 0, 0
regs = {chr(ord('a') + i): 0 for i in range(8)}


def fetch(i):
    try:
        i = int(i)
        return lambda: i
    except ValueError:
        return lambda: regs[i]


def op_set(x, y):
    regs[x] = y()


def op_sub(x, y):
    regs[x] -= y()


def op_mul(x, y):
    regs[x] *= y()
    global n_mul
    n_mul += 1


def op_jnz(x, y):
    global ip
    if x() != 0:
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
    fun = ops[op]
    return lambda: fun(x,y)


with open('23.in') as f:
    prog = tuple(parse(l) for l in f)

while 0 <= ip < len(prog):
    prog[ip]()
    ip += 1

print('Part 1:', n_mul)  # 4225
