#!/usr/bin/env python3


def run(lines, second=False):
    regs = {}
    if second:
        regs['c'] = 1
    lines = tuple(l.rstrip() for l in lines)
    pc = 0
    while 0 <= pc < len(lines):
        ops = lines[pc].split(' ')
        if ops[0] == 'jnz':
            try:
                test = int(ops[1])
            except ValueError:
                test = regs.setdefault(ops[1], 0)
            if test:
                pc += int(ops[2])
            else:
                pc += 1
        else:
            if ops[0] == 'cpy':
                try:
                    src = int(ops[1])
                except ValueError:
                    src = regs.setdefault(ops[1], 0)
                dst = ops[2]
                regs[dst] = src
            elif ops[0] == 'inc':
                dst = ops[1]
                regs[dst] = regs.get(dst, 0) + 1
            elif ops[0] == 'dec':
                dst = ops[1]
                regs[dst] = regs.get(dst, 0) - 1
            pc += 1
    return regs

test_input = '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''.split('\n')
assert(run(test_input)['a'] == 42)

with open('12.in') as f:
    print('Part 1:', run(f)['a'])  # 318117
    f.seek(0)
    print('Part 2:', run(f, second=True)['a'])  # 9227771 (slow)
