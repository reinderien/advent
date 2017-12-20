#!/usr/bin/env python3

import re


class Point:
    __slots__ = ('p', 'v', 'a', 'a_abs')
    parse = re.compile(r'[\d-]+')

    def __init__(self, line):
        nums = Point.parse.findall(line)
        self.p = [int(i) for i in nums[:3]]
        self.v = [int(i) for i in nums[3:6]]
        self.a = tuple(int(i) for i in nums[6:])
        self.a_abs = sum(abs(i) for i in self.a)


def p1(fname):
    """
                  2
      min[lim t→∞ ∑ | p_i + ∫v_i dt + ∫∫a_i dt |
                 i=0
           2
    ~ min[ ∑ a_i ]
          i=0
    """
    with open(fname) as f:
        return min((Point(l).a_abs, i) for i,l in enumerate(f))[1]

assert(p1('20.test.in') == 0)
print('Part 1:', p1('20.in'))  # 300
