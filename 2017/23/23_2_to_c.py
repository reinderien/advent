#!/usr/bin/env python3

gotos = set()
lines = []

with open('23.in', 'r') as fin:
    for lno, line in enumerate(fin):
        op, x, y = line.rstrip().split(' ')
        oline = '\t'
        if op == 'set':
            oline += '%s = %s' % (x, y)
        elif op == 'mul':
            oline += '%s *= %s' % (x, y)
        elif op == 'sub':
            oline += '%s -= %s' % (x, y)
        elif op == 'jnz':
            goto = lno+int(y)
            gotos.add(goto)
            oline += 'if (%s != 0) goto l%02d' % (x, goto)
        else:
            raise ValueError()
        oline += ';\t// %s' % line
        lines.append(oline)

with open('prog.c', 'w') as fout:
    for lno, line in enumerate(lines):
        if lno in gotos:
            fout.write('l%02d:%s' % (lno, line))
        else:
            fout.write('\t%s' % line)
    fout.write('l%02d: ;\n' % (lno+1))
