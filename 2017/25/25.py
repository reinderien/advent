#!/usr/bin/env python3

import re


class State:
    __slots__ = ('write_val', 'move', 'next_state')


def parse_line(pat, f):
    return re.search(pat, f.readline()).group(1)


def state_from_line(f):
    return ord(parse_line(r'state (\w)', f)) - ord('A')


def int_from_line(f):
    return int(parse_line(r'(\d+)', f))


def run(fname):
    states = []
    with open(fname) as f:
        state_id = state_from_line(f)
        n_iters = int_from_line(f)

        while f.readline():
            this_state_id = state_from_line(f)
            state_tests = [State(), State()]
            states.insert(this_state_id, state_tests)
            for _ in range(2):
                state = state_tests[int_from_line(f)]
                state.write_val = int_from_line(f)
                state.move = 1 if parse_line(r'to the (\w+)\.', f) == 'right' else -1
                state.next_state = state_from_line(f)

    tape = []
    pos = 0
    for cycle in range(n_iters):
        if pos < 0:
            tape[:0] = [0] * -pos
            pos = 0
        elif pos >= len(tape):
            tape.extend([0] * (pos - len(tape) + 1))

        state = states[state_id][tape[pos]]
        tape[pos] = state.write_val
        pos += state.move
        state_id = state.next_state

    return sum(tape)


assert(run('25.test.in') == 3)
print('Part 1:', run('25.in'))  # 4769
