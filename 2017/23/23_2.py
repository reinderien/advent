#!/usr/bin/env python3

with open('23.in', 'r') as fin, \
    open('prog.c', 'w') as fout:

    for lno, line in enumerate(fin):
        fout.write('l%02d:\t' % lno)
        op, x, y = line.rstrip().split(' ')
        if op == 'set':
            fout.write('%s = %s' % (x, y))
        elif op == 'mul':
            fout.write('%s *= %s' % (x, y))
        elif op == 'sub':
            fout.write('%s -= %s' % (x, y))
        elif op == 'jnz':
            fout.write('if (%s != 0) goto l%02d' % (x, lno+int(y)))
        fout.write(';\t// %s' % line)
    fout.write('l%02d: ;\n' % (lno+1))
