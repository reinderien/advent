#!/usr/bin/env python3

import re
from collections import deque
from time import time
from itertools import combinations
from pprint import pprint

'''
So this is a variant of the https://en.wikipedia.org/wiki/River_crossing_puzzle .

Rules:
- Get everything to floor 3 in min steps
- Elevator starts on floor 0
- Elevator must carry between one and two objects
- Elevator must move one floor at a time
- A chip cannot be with an incompatible gen unless also with its own gen
- The elevator is not isolated from the current floor

With an elevator, 5 generators and 5 chips spread out over 4 floors, the upper limit to the state
space size is
4^(1+2*5) = 4 194 304

State representation: a tuple, with the last entry being the elevator's floor;
even entries being the chip floors; and
odd entries being the generator floors.
'''


def run(fn):
    elements = []
    initial_state = [None]*10

    def add_elements(line, rex, offset, floor):
        for e in rex.findall(line):
            try:
                at = elements.index(e)
            except ValueError:
                at = len(elements)
                elements.append(e)
            initial_state[2*at + offset] = floor

    def parse():
        re_chip = re.compile(r'\w+(?=-compatible microchip)')
        re_gen = re.compile(r'\w+(?= generator)')
        floor = 0
        with open(fn) as f:
            for line in f:
                add_elements(line, re_chip, 0, floor)
                add_elements(line, re_gen, 1, floor)
                floor += 1

    def on_floor(state, floor):
        return set(o for o, f in enumerate(state[:-1]) if f == floor)

    # @profile
    def verify_state(on_this_floor):
        unshielded_chips = any(True for c in on_this_floor if (not c&1) and
                               (c+1) not in on_this_floor)
        has_gens = any(True for g in on_this_floor if g&1)

        return not (unshielded_chips and has_gens)

    # @profile
    def get_next_states(current):
        current_elev = current[-1]
        next_elevs = set()
        if current_elev > 0:
            next_elevs.add(current_elev - 1)
        if current_elev < 3:
            next_elevs.add(current_elev + 1)
        on_this_floor = on_floor(current, current_elev)
        carryable = {1}
        if len(on_this_floor) > 1:
            carryable.add(2)

        for next_elev in next_elevs:
            on_next_floor = on_floor(current, next_elev)
            for n_carried in carryable:
                for carried in combinations(on_this_floor, n_carried):
                    carried_set = set(carried)
                    if verify_state(on_this_floor - carried_set) and \
                            verify_state(on_next_floor | carried_set):
                        new_state = tuple(next_elev if o in carried_set else current[o]
                                          for o in range(len(current)-1)) + (next_elev,)
                        yield new_state

    # @profile
    def bfs():
        frontier_set = {initial_state}
        frontier_queue = deque((initial_state,))
        visited = set()
        paths = {}
        tick_time = time()
        while frontier_set:
            current = frontier_queue.popleft()
            frontier_set.remove(current)
            if current == end_state:
                path = []
                while current:
                    path = [current] + path
                    current = paths.get(current)
                return path
            next_states_yielded = get_next_states(current)
            next_states_set = set(next_states_yielded)
            next_states = next_states_set - visited - frontier_set
            paths.update((n, current) for n in next_states)
            frontier_set |= next_states
            frontier_queue.extend(next_states)
            visited.add(current)

            new_tick_time = time()
            if new_tick_time - tick_time >= 1:
                tick_time = new_tick_time
                print('Paths: %d  Visited: %d  Frontier: %d    ' %
                      (len(paths), len(visited), len(frontier_set)), end='\r')

    def results(path):
        print()
        print_elements(elements)
        steps = len(path) - 1
        print('Steps:', steps)
        pprint(path)
        return steps

    parse()
    initial_state = (*initial_state[:2 * len(elements)], 0)  # add elevator
    end_state = (3,) * len(initial_state)
    return results(bfs())


def print_elements(elements):
    print(', '.join('{0:s} chip, {0:s} gen'.format(e)
                    for e in elements)
          + ', elevator')

print('Part 1 test ---')
test_steps = run('11-test.in')
assert(test_steps == 11)

print('Part 1 ---')
run('11.in')  # 35 is not correct
