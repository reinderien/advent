#!/usr/bin/env python3


def run(val_a, val_b):
    matches = 0
    for _ in range(40_000_000):  # Way too slow
        val_a = 16807*val_a % 0x7FFF_FFFF
        val_b = 48271*val_b % 0x7FFF_FFFF
        matches += val_a&0xFFFF == val_b&0xFFFF
        continue
    return matches

assert(run(65, 8921) == 588)
print('Part 1:', run(618, 814))  # 577
