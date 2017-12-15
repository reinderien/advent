#!/usr/bin/env python3


def run(fname):
    sev = 0
    with open(fname) as f:
        for line in f:
            t, s_range = (int(i) for i in line.rstrip().split(': '))
            r = s_range-1
            scanner = r - abs(r - t%(2*r))
            if scanner == 0:
                sev += s_range*t
    return sev

assert(run('13.test.in') == 24)
print('Part 1:', run('13.in'))  # 1612

