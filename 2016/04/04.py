#!/usr/bin/env python3

import re

sect_sum = 0
for line in open('04.in'):
    name, sect, cs = re.match(r'^(.+)-(\d+)\[(.+)\]$', line).groups()
    sect = int(sect)
    letters = set(c for c in name if c != '-')
    freqs = sorted((sum(-1 for d in name if d==c), c) for c in letters)
    actcs = ''.join([f[1] for f in freqs][:5])
    if actcs == cs:
        sect_sum += sect

    plaintext = ''.join(
        ' ' if c == '-' else
            chr((ord(c)-ord('a')+sect)%26 + ord('a'))
        for c in name
    )
    if plaintext == 'northpole object storage':
        print('#2: %d' % sect)

print('#1: %d' % sect_sum)  # 361724 - correct
