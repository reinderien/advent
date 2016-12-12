#!/usr/bin/env python3

import re

line = open('09.in').read().strip()
dec_len, zip_i = 0, 0
marker = re.compile(r'\((\d+)x(\d+)\)')

while True:
    match = marker.search(line, zip_i)
    if match:
        span, rep = (int(g) for g in match.groups())
        dec_len += match.start() - zip_i + span*rep
        zip_i = match.end() + span
    else:
        dec_len += len(line) - zip_i
        break
print(dec_len)  # 152851 is correct
