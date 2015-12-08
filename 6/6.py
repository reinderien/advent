#!/usr/bin/env python3
# http://adventofcode.com/day/6

from re import match

rects = set()

class Rect:
    def __init__(self, x0,y0,x1,y1):
        self.x0,self.y0,self.x1,self.y1 = x0,x1,y0,y1

    def overlaps(self, r):
        return (r.x1 >= self.x0 and
                r.y1 >= self.y0 and
                r.x0 <= self.x1 and
                r.y0 <= self.y1)
    def ok(self):
        return self.x0 < self.x1 and self.y0 < self.y1


for line in open('6.in').readlines():
    groups = match(
        r'^(?P<action>.+) '
        r'(?P<x0>\d+),(?P<y0>\d+) through '
        r'(?P<x1>\d+),(?P<y1>\d+)$', line).group
    action = groups('action')
    s = Rect(int(groups('x0')), int(groups('y0')),
             int(groups('x1')), int(groups('y1')))
    to_add, to_remove = set(), set()

    for r in rects:
        if r.overlaps(s):
            '''
            Break up rect and keep all non-overlapping parts
                ______
            ___|_     |
            |s  | r   |
            -----     |
               |______|

            _____________________
            |_______rup__________|
            |rleft|      |rright |
            |     |  s   |       |
            |     |      |       |
            |____________________|
            |     rdown          |
            |____________________|

            4x edge in
            4x edge out
            4x corner
            2x through
            1x in
            1x out
            Best case, no action
            Worst case, split r to 4 new rects
            '''
            rleft  = Rect(r.x0  , s.y0  , s.x0-1, s.y1  )
            rright = Rect(s.x0+1, s.y0  , r.x1  , s.y1  )
            rdown  = Rect(r.x0  , r.y0  , r.x1  , s.y0-1)
            rup    = Rect(r.x0  , s.y1+1, r.x1  , r.y1  )
            all_sides = {rleft, rright, rdown, rup}
            oks = {x for x in all_sides if x.ok()}

            if action == 'turn on':
                if any(not x.ok() for x in all_sides):
                    to_remove.add(r)
                    to_add.add(s)
                    to_add |= oks
            elif action == 'turn off':
                to_remove.add(r)
                to_add |= oks
            elif action == 'toggle':
                to_remove.add(r)
                tleft  = Rect(s.x0  , s.y0  , r.x0-1, s.y1  )
                tright = Rect(r.x1+1, s.y0  , s.x1  , s.y1  )
                tdown  = Rect(s.x0  , s.y0  , s.x1  , r.y0-1)
                tup    = Rect(s.x0  , r.y1+1, s.x1  , s.y1  )
                to_add |= oks | {t for t in (tleft, tright, tdown, tup) if t.ok()}













# Should be 377891