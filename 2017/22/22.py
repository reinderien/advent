#!/usr/bin/env python3


def run(fname, p2=False):
    with open(fname) as f:
        ''' 0: clean
            1: weakened
            2: infected
            3: flagged
        '''
        grid = [list(2 if c == '#' else 0
                     for c in line.rstrip())
                for line in f]

    x = len(grid[0])//2        # x-coord current pos
    y = len(grid)//2           # y-coord current pos
    deltas = ((0,-1), ( 1,0),  # up, right,
              (0, 1), (-1,0))  # down, left vectors
    i_delta = 0                # start dir index facing up
    caused = 0                 # infections caused
    n_iters = 10_000_000 if p2 else 10_000

    def grow():
        nonlocal x, y, grid
        while x < 0:
            for ya in range(len(grid)):
                grid[ya].insert(0, 0)
            x += 1
        while x >= len(grid[0]):
            for ya in range(len(grid)):
                grid[ya].append(0)
        while y < 0:
            grid.insert(0, [0] * len(grid[0]))
            y += 1
        while y >= len(grid):
            grid.append([0] * len(grid[0]))

    for it in range(n_iters):
        c = grid[y][x]         # Old state
        if p2:
            c_new = (c+1) & 3  # Through all 4 states
        else:
            c_new = 2 - c      # Infected <-> clean
        caused += c_new == 2   # Track infections
        grid[y][x] = c_new     # Store state
        if p2:
            c_del = c - 1      # Left, straight, right, reverse
        else:
            c_del = 1 if c == 2 else -1  # Turn left or right
        i_delta = (i_delta + c_del) % 4  # New direction index
        delta = deltas[i_delta]          # New direction vector
        x += delta[0]                    # Move x in new dir
        y += delta[1]                    # Move y in new dir
        grow()

        if not (it & 0xFFFFF):
            print('%.1f%% ' % (it * 100 / n_iters), end='\r')
    print()
    return caused

assert(run('22.test.in') == 5587)
print('Part 1:', run('22.in'))  # 5240
assert(run('22.test.in', p2=True) == 2_511_944)
print('Part 2:', run('22.in', p2=True))  # 2512144
