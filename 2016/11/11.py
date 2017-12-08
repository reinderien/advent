#!/usr/bin/env python3

'''
Positive generator, negative chip.
By atomic number,
    38 Strontium
    44 Ruthenium
    61 Promethium
    69 Thulium
    94 Plutonium
'''

floors = (
    { 69, -69, 94, 38},
    {-94, -38},
    { 61, -61, 44, -44},
    set()
)

objects = {o: i for i, objs in enumerate(floors)
           for o in objs}

