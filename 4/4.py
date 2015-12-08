#!/usr/bin/env python3
# http://adventofcode.com/day/4

from hashlib import md5
from struct import unpack

prefix, ans = 'ckczppom', 0

mask = 0xFFFFFF00  # yields 3938038
# mask = 0xFFFFF000  # yields 117946

while True:
    hash = md5(bytes(prefix + str(ans), 'ascii')).digest()
    data = unpack('>LLLL', hash)
    if not (data[0] & mask): break
    ans += 1
    if not (ans % 10000): print('\r%d    ' % ans, end='')
print(ans)
