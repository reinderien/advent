#!/usr/bin/env python3

import re

'''
So this is a variant of the https://en.wikipedia.org/wiki/River_crossing_puzzle .

Rules:
- Get everything to floor 3 in min steps
- Elevator starts on floor 0
- Elevator must carry between one and two objects
- Elevator must move one floor at a time
- A chip cannot be with an incompatible gen unless also with its own gen
- The elevator is not isolated from the current floor



Positive generator, negative chip.
'''


def run(fn):
    elements = {
        'hydrogen': 1,
        'lithium': 3,
        'strontium': 38,
        'ruthenium': 44,
        'promethium': 61,
        'thulium': 69,
        'plutonium': 94
    }

    objects = {}

    def parse():
        re_chip = re.compile(r'\w+(?=-compatible microchip)')
        re_gen = re.compile(r'\w+(?= generator)')
        floor = 0
        with open(fn) as f:
            for line in f:
                objects.update((elements[e], floor)
                               for e in re_gen.findall(line))
                objects.update((-elements[e], floor)
                               for e in re_chip.findall(line))
                floor += 1
    parse()
    return

assert(run('11-test.in') == 11)
print('Part 1:', run('11.in'))
