#!/usr/bin/env python3

from hashlib import md5
from struct import unpack

prefix, ans = 'ckczppom', 0

# mask = 0xFFFFF000  # yields 117946
mask = 0xFFFFFF00  # yields 3938038

while True:
    hash = md5(bytes(prefix + str(ans), 'ascii')).digest()
    data = unpack('>LLLL', hash)
    if not (data[0] & mask): break
    ans += 1
    if not (ans % 20000): print('\r%d..' % ans, end='')
print('\n%d' % ans)
