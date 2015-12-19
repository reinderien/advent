#!/usr/bin/env python3

part = 2


def evolve(state):
    new_state = []
    for y in range(len(state)):
        new_line = ''
        for x in range(len(state[0])):
            n_others = 0
            for yo in range(y-1,y+2):
                for xo in range(x-1,x+2):
                    if (0 <= yo < len(state) and 0 <= xo < len(state[0]) and
                       not (yo == y and xo == x) and state[yo][xo] == '#'):
                        n_others += 1
            if state[y][x] == '#':
                alive = 2 <= n_others <= 3
            else: alive = n_others == 3
            if alive: new_line += '#'
            else: new_line += '.'
        new_state.append(new_line)
    return new_state

corners = ((0,0), (0,99), (99,0), (99,99))

def evolve2(state):
    new_state = []
    for y in range(len(state)):
        new_line = ''
        for x in range(len(state[0])):
            if (x,y) in corners:
                alive = True
            else:
                n_others = 0
                for yo in range(y-1,y+2):
                    for xo in range(x-1,x+2):
                        if (0 <= yo < len(state) and 0 <= xo < len(state[0]) and
                           not (yo == y and xo == x) and state[yo][xo] == '#'):
                            n_others += 1
                if state[y][x] == '#':
                    alive = 2 <= n_others <= 3
                else: alive = n_others == 3
            if alive: new_line += '#'
            else: new_line += '.'
        new_state.append(new_line)
    return new_state


def count(state):
    return sum(1 for l in state for c in l if c == '#')

'''
test_state = (
    '.#.#.#',
    '...##.',
    '#....#',
    '..#...',
    '#.#..#',
    '####..'
)
for _ in range(6):
    print('\n'.join(test_state) + ' %d\n' % count(test_state))
    test_state = evolve(test_state)
'''

file_state = [l.rstrip() for l in open('18.in').readlines()]

if part == 2:
    for y in (0, 99):
        file_state[y] = '#' + file_state[y][1:99] + '#'

for _ in range(100):
    if part == 1:
        file_state = evolve(file_state)
    else:
        file_state = evolve2(file_state)

# 1: 821
# 2: 886
print(count(file_state))
