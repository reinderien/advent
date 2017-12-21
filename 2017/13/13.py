#!/usr/bin/env python3

from itertools import count


def run(fname):
    with open(fname) as f:
        scanners = tuple(tuple(int(i) for i in line.rstrip().split(': '))
                         for line in f)

    def get_sev(delay=0):
        sev = 0
        for t, s_range in scanners:
            r = s_range-1
            scanner = r - abs(r - (t+delay) % (2*r))
            if scanner == 0:
                sev += s_range*t
        return sev

    def dodge():
        for delay in count():
            for t, s_range in scanners:
                r = s_range-1
                scanner = r - abs(r - (t+delay) % (2*r))
                if scanner == 0:
                    break
            else:
                return delay

    return get_sev(), dodge()

assert(run('13.test.in') == (24, 10))
print('Parts 1, 2:', run('13.in'))  # 1612, 3907994
