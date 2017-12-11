#!/usr/bin/env python3

from functools import reduce
from operator import xor
from binascii import hexlify


def do_round(lengths, hash_len, hash_seq=None, pos=0, skip=0):
    if hash_seq is None:
        hash_seq = bytearray(range(hash_len))
    for length in lengths:
        hash_seq[:length] = hash_seq[length - hash_len - 1::-1]
        delta = (length + skip) % hash_len
        hash_seq = hash_seq[delta:] + hash_seq[:delta]
        pos = (pos + delta) % hash_len
        skip += 1
    return hash_seq, pos, skip


def p1(lengths, hash_len=256):
    lengths = [int(n) for n in lengths.split(',')]
    hash_seq, pos, skip = do_round(lengths, hash_len)
    return hash_seq[hash_len - pos] * hash_seq[hash_len - pos + 1]


def p2(byte_string, hash_len=256):
    lengths = bytearray(byte_string, 'ascii') + bytes((17, 31, 73, 47, 23))
    sparse_hash, pos, skip = do_round(lengths, hash_len)
    for _ in range(1, 64):
        sparse_hash, pos, skip = do_round(lengths, hash_len, sparse_hash, pos, skip)

    sparse_hash = sparse_hash[-pos:] + sparse_hash[:-pos]
    dense_hash = bytearray(reduce(xor, sparse_hash[i:i+16])
                           for i in range(0, hash_len, 16))
    return hexlify(dense_hash)


real_input = '34,88,2,222,254,93,150,0,199,255,39,32,137,136,1,167'

assert(p1('3,4,1,5', 5) == 12)
print('Part 1:', p1(real_input))  # 54675

print('Part 2:', p2(real_input))  # a7af2706aa9a09cf5d848c1e6605dd2a
