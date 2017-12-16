#!/usr/bin/env python3


def run(text, n):
    names = [chr(ord('a') + i) for i in range(n)]

    for op in text.split(','):
        if op[0] == 's':
            s = n - int(op[1:])
            names = names[s:] + names[:s]
        elif op[0] == 'x':
            a, b = (int(i) for i in op[1:].split('/'))
            names[a], names[b] = names[b], names[a]
        elif op[0] == 'p':
            a, b = op[1], op[3]
            ia, ib = names.index(a), names.index(b)
            names[ia], names[ib] = b, a
    return ''.join(names)

assert(run('s1,x3/4,pe/b', 5) == 'baedc')
with open('16.in') as f:
    print('Part 1:', run(f.read(), 16))  # kgdchlfniambejop
