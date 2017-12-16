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


def run(key):
    used = 0
    for row in range(128):
        for byte in knot('%s-%d' % (key, row)):
            while byte:
                if byte & 1:
                    used += 1
                byte >>= 1
    return used

assert(run('flqrgnkx') == 8108)
print('Part 1:', run('hwlqcszp'))  # 8304
