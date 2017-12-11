#!/usr/bin/env python3


def run(list_len, lengths):
    pos, skip = 0, 0
    data = list(range(list_len))
    for length in lengths:
        data[:length] = data[length-list_len-1::-1]
        delta = (length + skip) % list_len
        data = data[delta:] + data[:delta]
        pos = (pos + delta) % list_len
        skip += 1
    return data[-pos:] + data[:-pos]


def p1(list_len, lengths):
    data = run(list_len, lengths)
    print('Part 1:', data[0] * data[1])

real_input = (34,88,2,222,254,93,150,0,199,255,39,32,137,136,1,167)

print('Test:')  # 12
p1(5, (3, 4, 1, 5))
print('Real:')  # 54675
p1(256, real_input)
