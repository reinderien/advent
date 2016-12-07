#!/usr/bin/env python3

import re

# { pers1 name: { neighbour name: effect object, ... }, ... }
effects = {}
all_names = set()


class Effect:
    line_format = re.compile(
        r'^(.+) would (gain|lose) (\d+) happiness units by sitting next to (.+)\.$')

    def __init__(self, line):
        self.pers1, neg, amount, self.pers2 = self.line_format.match(line).groups()
        self.amount = int(amount)
        if neg == 'lose':
            self.amount = -self.amount
        effects.setdefault(self.pers1, {})[self.pers2] = self
        all_names.add(self.pers1)


for inline in open('13.in').readlines():
    Effect(inline)


def recurse(used_names, avail_names=None, old_change=0):
    # I could write an early boundary termination condition to speed this up, but eff it

    if avail_names is None:
        avail_names = all_names - set(used_names)
    elif len(avail_names) == 0:
        return old_change, used_names

    best_change, best_names = float('-inf'), None
    for new_neighbour in avail_names:
        new_change = old_change + (
            effects[new_neighbour][used_names[-1]].amount +
            effects[used_names[-1]][new_neighbour].amount)
        if len(avail_names) == 1:
            new_change += (
                effects[used_names[0]][new_neighbour].amount +
                effects[new_neighbour][used_names[0]].amount)
        total_change, total_names = recurse(used_names=used_names + [new_neighbour],
                                            avail_names=avail_names - {new_neighbour},
                                            old_change=new_change)
        if best_change < total_change:
            best_change, best_names = total_change, total_names
    return best_change, best_names


def dump(change, names):
    print('%d: ' % change, end='')
    for i, name in enumerate(names):
        print('%d/%s/%d ' % (
            effects[name][names[(i - 1) % len(all_names)]].amount,
            name,
            effects[name][names[(i + 1) % len(all_names)]].amount), end='')
    print()

# 664: -20/David/43 65/Alice/-2 93/Bob/23 76/George/54 34/Eric/95 -17/Frank/-9 33/Carol/10 95/Mallory/91
top_change, top_names = recurse(used_names=list(effects.keys())[:1])
dump(top_change, top_names)

old_names = set(all_names)
for neighbour_name in old_names:
    Effect('me would gain 0 happiness units by sitting next to %s.' % neighbour_name)
    Effect('%s would gain 0 happiness units by sitting next to me.' % neighbour_name)
best_fix_change, best_fix_names = float('inf'), None
for insertion in range(len(old_names)):
    n1, n2 = top_names[insertion], top_names[(insertion-1) % len(top_names)]
    fix_change = effects[n1][n2].amount + effects[n2][n1].amount
    if best_fix_change > fix_change:
        best_fix_change = fix_change
        best_fix_names = top_names[:insertion] + ['me'] + top_names[insertion:]

# 640: -20/David/43 65/Alice/-2 93/Bob/23 76/George/54 34/Eric/95 -17/Frank/0 0/me/0 0/Carol/10 95/Mallory/91
# 24 change due to insertion of me
dump(top_change - best_fix_change, best_fix_names)
print('%d change due to insertion of me' % best_fix_change)
