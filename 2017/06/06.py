#!/usr/bin/env python3


def run(banks):
    seen = {}
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
        seen_cycles = seen.get(bank_check)
        if seen_cycles:
            return cycles, cycles - seen_cycles, bank_check
        seen[bank_check] = cycles


assert(run([0,2,7,0]) == (5, 4, (2,4,1,2)))
with open('06.in') as f:
    file_banks = [int(b) for b in f.read().split()]
file_cycles, file_loop, _ = run(file_banks)
print('Part 1:', file_cycles)  # 12841
print('Part 2:', file_loop)    # 8038
