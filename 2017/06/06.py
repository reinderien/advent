#!/usr/bin/env python3


def run(banks):
    seen = set()
    cycles = 0
    while True:
        i, v = max(enumerate(banks), key=lambda v: v[1])
        banks[i] = 0
        while v > 0:
            i = (i + 1) % len(banks)
            v -= 1
            banks[i] += 1

        cycles += 1
        bank_check = tuple(banks)
        if bank_check in seen:
            return cycles, bank_check
        seen.add(bank_check)


assert(run([0,2,7,0]) == (5, (2,4,1,2)))
with open('06.in') as f:
    file_banks = [int(b) for b in f.read().split()]
file_cycles, _ = run(file_banks)
print('Part 1:', file_cycles)  # 12841

