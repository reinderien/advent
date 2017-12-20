#!/usr/bin/env python3

import re
from itertools import count


class Point:
    __slots__ = ('p', 'v', 'a', 'a_abs')
    parse = re.compile(r'[\d-]+')

    def __init__(self, line):
        nums = Point.parse.findall(line)
        self.p = [int(i) for i in nums[:3]]
        self.v = [int(i) for i in nums[3:6]]
        self.a = tuple(int(i) for i in nums[6:])
        self.a_abs = sum(abs(i) for i in self.a)

    def __str__(self):
        return 'p=<%s>, v=<%s>, a=<%s>' % (
            ','.join(str(p) for p in self.p),
            ','.join(str(v) for v in self.v),
            ','.join(str(a) for a in self.a)
        )

    def tick(self):
        for i,a in enumerate(self.a):
            v = self.v[i]
            v += a
            self.v[i] = v
            self.p[i] += v


def p1(fname):
    """
                  2
      min[lim t→∞ ∑ | p_i + ∫v_i dt + ∫∫a_i dt |
                 i=0
           2
    ~ min[ ∑ |a_i| ]
          i=0
    """
    with open(fname) as f:
        return min((Point(l).a_abs, i) for i,l in enumerate(f))[1]


def p2(fname):
    """
    The smart thing to do is to detect when points are diverging and remove them from the
    collision culling loop. But this algo does not do anything smart. It performs a braindead
    stability heuristic... and gets the right answer.
    """
    with open(fname) as f:
        points = [Point(l) for l in f]

    old_len = len(points)
    changed = 0

    for iters in count():
        for point in points:
            point.tick()

        posns, collided = set(), set()
        for posn in (tuple(p.p) for p in points):
            if posn in posns:
                posns.remove(posn)
                collided.add(posn)
            elif posn not in collided:
                posns.add(posn)
        points = [p for p in points if tuple(p.p) not in collided]

        new_len = len(points)
        if old_len > new_len:
            old_len = new_len
            changed = iters
        elif iters - changed > 10:  # loooool
            return len(points)


assert(p1('20.test.in') == 0)
print('Part 1:', p1('20.in'))  # 300
print('Part 2:', p2('20.in'))  # 502
