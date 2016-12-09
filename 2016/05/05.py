#!/usr/bin/env python3

# Broken; see C impl

from hashlib import md5

id = b'wtnhxymk'
idx = 0
comp = b'\x00'*5
for _ in range(8):
    while True:
        hash = md5(id + bytes(str(idx), 'ascii')).digest()
        idx += 1
        if hash[:5] == comp:
            print(hash)
            print(idx)
            exit()
