#!/usr/bin/env python3


def run(fname):
    with open(fname) as f:
        ops = tuple(line.rstrip().split(' ') for line in f)
    for op in ops:
        for i,v in enumerate(op):
            try:
                op[i] = int(v)
            except ValueError:
                pass

    regs = {}
    pc = 0
    last_freq = None

    def maybe_reg(name):
        if isinstance(name, int):
            return name
        return regs.get(name, 0)

    while 0 <= pc < len(ops):
        op = ops[pc]
        if op[0] == 'jgz':
            test = maybe_reg(op[1])
            if test > 0:
                pc += op[2]
            else:
                pc += 1
        else:
            if op[0] == 'snd':
                last_freq = maybe_reg(op[1])
            elif op[0] == 'set':
                regs[op[1]] = maybe_reg(op[2])
            elif op[0] == 'add':
                regs[op[1]] = regs.setdefault(op[1], 0) + maybe_reg(op[2])
            elif op[0] == 'mul':
                regs[op[1]] = regs.setdefault(op[1], 0) * maybe_reg(op[2])
            elif op[0] == 'mod':
                regs[op[1]] = regs.setdefault(op[1], 0) % maybe_reg(op[2])
            elif op[0] == 'rcv':
                if maybe_reg(op[1]):
                    return last_freq
            pc += 1

    raise IndexError('Program terminated without a rcv')

assert(run('18.test.in') == 4)
print('Part 1:', run('18.in'))  # 2951
