#!/usr/bin/env python3

from timeit import timeit
from subprocess import check_call
from pprint import pprint

cmds = [(i, '{:02d}.py'.format(i)) for i in (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 19, 20
)] + [( 5, '05_2'),
      (16, '16_1.py'),
      (16, '16_2.py'),
      (17, '17_2'),
      (18, '18.1.py'),
      (18, '18.2.py')]


def run(d, c):
    print(c, end='')
    if c.endswith('.py'):
        args = ('/usr/bin/python3', c)
    else:
        args = ('./' + c,)
    t = timeit(lambda: check_call(args, cwd='./{:02d}'.format(d)), number=1)
    print('   %f' % t)
    return t, d, c

times = tuple(sorted(run(d, c) for d,c in cmds))
pprint(times)
