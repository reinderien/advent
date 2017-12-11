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
    data = data[-pos:] + data[:-pos]
    print('Part 1:', data[0] * data[1])


print('Test:')  # 12
run(5, (3, 4, 1, 5))
print('Real:')  # 54675
run(256, (34,88,2,222,254,93,150,0,199,255,39,32,137,136,1,167))
