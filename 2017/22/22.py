#!/usr/bin/env python3


def run(fname):
    with open(fname) as f:
        grid = [list(1 if c == '#' else 0
                     for c in line.rstrip())
                for line in f]

    x = len(grid[0])//2        # x-coord current pos
    y = len(grid)//2           # y-coord current pos
    deltas = ((0,-1), ( 1,0),  # up, right,
              (0, 1), (-1,0))  # down, left vectors
    i_delta = 0                # start dir index facing up
    caused = 0                 # infections caused

    for _ in range(10_000):
        c = grid[y][x]                   # Old state
        c_new = 1 - c                    # New state
        caused += c_new                  # Track infections
        grid[y][x] = c_new               # Store state
        c_del = 1 if c else -1           # Turn left or right
        i_delta = (i_delta + c_del) % 4  # New direction index
        delta = deltas[i_delta]          # New direction vector
        x += delta[0]                    # Move x in new dir
        y += delta[1]                    # Move y in new dir

        # Grow grid as necessary
        while x < 0:
            for ya in range(len(grid)):
                grid[ya].insert(0, 0)
            x += 1
        while x >= len(grid[0]):
            for ya in range(len(grid)):
                grid[ya].append(0)
        while y < 0:
            grid.insert(0, [0]*len(grid[0]))
            y += 1
        while y >= len(grid):
            grid.append([0]*len(grid[0]))
    return caused

assert(run('22.test.in') == 5587)
print('Part 1:', run('22.in'))  # 5240
