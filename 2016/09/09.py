#!/usr/bin/env python3

import re

marker = re.compile(r'\((\d+)x(\d+)\)')


def dec(line):
    dec_len, zip_i = 0, 0

    while True:
        match = marker.search(line, zip_i)
        if match:
            span, rep = (int(g) for g in match.groups())
            dec_len += match.start() - zip_i + span*rep
            zip_i = match.end() + span
        else:
            dec_len += len(line) - zip_i
            return dec_len


def dec2(line):
    def recurse(i_start, i_end):
        dec_len = 0
        while True:
            match = marker.search(line, i_start, i_end)
            if not match:
                return dec_len + i_end - i_start
            span, rep = (int(g) for g in match.groups())
            i_new_start = match.end() + span
            dec_len += match.start() - i_start + rep*recurse(i_start=match.end(),
                                                             i_end=i_new_start)
            i_start = i_new_start
    return recurse(0, len(line))


with open('09.in') as f:
    file_line = f.read().strip()

assert(dec('ADVENT') == 6)
assert(dec('A(1x5)BC') == 7)
assert(dec('(3x3)XYZ') == 9)
assert(dec('A(2x2)BCD(2x2)EFG') == 11)
assert(dec('(6x1)(1x3)A') == 6)
assert(dec('X(8x2)(3x3)ABCY') == 18)
print('Part 1:', dec(file_line))  # 152851

assert(dec2('(3x3)XYZ') == 9)
assert(dec2('X(8x2)(3x3)ABCY') == 20)
assert(dec2('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920)
assert(dec2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445)
print('Part 2:', dec2(file_line))  # 11797310782
