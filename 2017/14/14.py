#!/usr/bin/env python3

from functools import reduce
from operator import xor


def knot(byte_string):
    lengths = bytearray(byte_string, 'ascii') + bytes((17, 31, 73, 47, 23))
    hash_seq = bytearray(range(256))
    pos, skip = 0, 0
    for _ in range(64):
        for length in lengths:
            hash_seq[:length] = hash_seq[length - 256 - 1::-1]
            delta = (length + skip) % 256
            hash_seq = hash_seq[delta:] + hash_seq[:delta]
            pos = (pos + delta) % 256
            skip += 1
    hash_seq = hash_seq[-pos:] + hash_seq[:-pos]
    return bytearray(reduce(xor, hash_seq[i:i+16]) for i in range(0, 256, 16))


def get_hashes(key):
    return tuple(knot('%s-%d' % (key, row))
                 for row in range(128))


def p1(hashes):
    used = 0
    for row in hashes:
        for byte in row:
            while byte:
                if byte & 1:
                    used += 1
                byte >>= 1
    return used


def p2(hashes, show=False):
    # 128^2 * 64 bytes per tuple of two ints. Worst case on the order of 1MB.
    # Submit all complaints to /dev/null.
    used_coords = {
        (bit + 8*x, y)
        for y, row in enumerate(hashes)
        for x, byte in enumerate(row)
        for bit in range(8)
        if (byte >> (7 - bit)) & 1
    }

    n_groups = 0
    deltas = ((-1, 0), (0, -1),
              ( 1, 0), (0,  1))

    def recurse(x, y):
        for dx, dy in deltas:
            new = (x+dx, y+dy)
            if new in used_coords:
                used_coords.remove(new)
                recurse(*new)

    while used_coords:
        current = used_coords.pop()
        recurse(*current)
        n_groups += 1
    return n_groups

test_hashes = get_hashes('flqrgnkx')
real_hashes = get_hashes('hwlqcszp')
assert(p1(test_hashes) == 8108)
print('Part 1:', p1(real_hashes))  # 8304
assert(p2(test_hashes) == 1242)
print('Part 2:', p2(real_hashes))  # 1018
