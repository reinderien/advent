#!/usr/bin/env python3

from math import ceil, sqrt


def op(lhs, at=0):
    return tuple(int(l[2]) for l in lines if l[0] == lhs)[at]

# Don't go overboard with auto-optimization of the program, but let's at least get this from the
# file

with open('23.in') as f:
    lines = tuple(l.rstrip().rpartition(' ') for l in f)
first_prime = op('set b')*op('mul b') - op('sub b')
last_prime = first_prime - op('sub c')
pitch = -op('sub b', 1)

sieve = [1]*(last_prime + 1)
base_max = int(ceil(sqrt(last_prime)))
for b in range(2, base_max):
    if sieve[b]:
        for f in range(b*b, last_prime+1, b):
            sieve[f] = 0

non_primes = sum(1-sieve[f] for f in range(first_prime, last_prime+1, pitch))

print('Part 2:', non_primes)  # 905
