#!/usr/bin/env python3

dirs = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}


def solve(part):
    if part == 1:
        digits = ('     ',
                  ' 123 ',
                  ' 456 ',
                  ' 789 ',
                  '     ')
    else:
        digits = ('       ',
                  '   1   ',
                  '  234  ',
                  ' 56789 ',
                  '  ABC  ',
                  '   D   ',
                  '       ')
    for line in open('02.in'):
        y = int(len(digits)/2)
        x = y
        for c in line.strip():
            dx, dy = dirs[c]
            nx, ny = x+dx, y+dy
            if digits[ny][nx] != ' ':
                x, y = nx, ny
        print(digits[y][x], end='')
    print()

solve(1)  # 38961 - correct
solve(2)  # 46C92 - correct
