#!/usr/bin/env python3

import re


def parse_pos(pos_from, pos_to):
    pos_from, pos_to = int(pos_from), int(pos_to)
    if pos_from > pos_to:
        pos_from, pos_to = pos_to, pos_from
    return pos_from, pos_to


def swap_pos(pwd, pos_from, pos_to):
    pos_from, pos_to = parse_pos(pos_from, pos_to)
    pwd[pos_from], pwd[pos_to] = pwd[pos_to], pwd[pos_from]
    return pwd


def swap_letter(pwd, let_from, let_to):
    pos_from, pos_to = pwd.index(let_from), pwd.index(let_to)
    pwd[pos_from], pwd[pos_to] = pwd[pos_to], pwd[pos_from]
    return pwd


def rotate_pos(pwd, dirn, steps):
    steps = int(steps) % len(pwd)
    if dirn == 'right':
        steps = -steps
    return pwd[steps:] + pwd[:steps]


def rotate_letter(pwd, let):
    pos = pwd.index(let)
    if pos >= 4:
        pos += 1
    return rotate_pos(pwd, 'right', pos + 1)


def reverse(pwd, pos_from, pos_to):
    pos_from, pos_to = parse_pos(pos_from, pos_to)
    pwd[pos_from: pos_to+1] = list(reversed(pwd[pos_from: pos_to+1]))
    return pwd


def move(pwd, pos_from, pos_to):
    pos_from, pos_to = int(pos_from), int(pos_to)
    pwd.insert(pos_to, pwd.pop(pos_from))
    return pwd


def run(fname, start):
    pwd = list(start)

    ops = (
        (re.compile(r'swap position (\d+) with position (\d+)'), swap_pos),
        (re.compile(r'swap letter (\w) with letter (\w)'),       swap_letter),
        (re.compile(r'rotate (left|right) (\d+) step'),          rotate_pos),
        (re.compile(r'rotate based on position of letter (\w)'), rotate_letter),
        (re.compile(r'reverse positions (\d+) through (\d+)'),   reverse),
        (re.compile(r'move position (\d+) to position (\d+)'),   move)
    )

    with open(fname) as f:
        for line in f:
            line = line.rstrip()
            for rex, fun in ops:
                m = rex.match(line)
                if m:
                    pwd = fun(pwd, *m.groups())
                    break
            else:
                raise ValueError('"%s" failed to parse' % line)
            # print('%s %s' % (''.join(pwd), line))
            assert(len(pwd) == len(start))

    return ''.join(pwd)


assert(run('test_input.txt', 'abcde') == 'decab')
print(run('input.txt', 'abcdefgh'))
