#!/usr/bin/env python3

import re
from collections import defaultdict, deque
from hashlib import md5
from itertools import count


class Quint:
    __slots__ = ('index', 'letter')


def run(salt, p2=False):
    re_triple = re.compile(r'(.)\1{2}')  # Three hexits in a row
    re_quint = re.compile(r'(.)\1{4}')   # Five hexits in a row
    quints_q = deque()           # Queue of quintuples among next 1000 hashes
    quints_d = defaultdict(set)  # {hexit: set(quintuples)} within next 1000 hashes
    hashes = deque()             # Queue of next 1000 hashes
    keys = 0                     # Number of keys found
    base_hash = md5()            # Hash of prefix salt
    base_hash.update(salt.encode('ascii'))

    def get_hash(ind):
        rounds = 2017 if p2 else 1
        m = base_hash.copy()
        inp = str(ind)
        for _ in range(rounds):
            m.update(inp.encode('ascii'))
            inp = m.hexdigest()
            m = md5()
        return inp

    def add_quint(ind, md):
        mat = re_quint.search(md)
        if mat:
            q = Quint()
            q.index = ind
            q.letter = mat.group(1)
            quints_q.append(q)
            quints_d[q.letter].add(q)

    for index in range(1000):
        mdval = get_hash(index)  # md5 of salt+index, as hex string
        hashes.append(mdval)     # store in hash queue
        add_quint(index, mdval)  # if it's a quint, save it

    for index in count():
        while quints_q:          # purge old quints
            oldest = next(iter(quints_q))
            if oldest.index > index:
                break
            quints_q.popleft()
            quints_d[oldest.letter].remove(oldest)
        last_index = index + 1000         # last index of the window
        last_hash = get_hash(last_index)  # hash at the end
        add_quint(last_index, last_hash)  # save if it's a quint
        hashes.append(last_hash)          # save the hash

        this_hash = hashes.popleft()            # take the first hash in the queue
        match = re_triple.search(this_hash)     # check if a triple
        if match and quints_d[match.group(1)]:  # look for quint matches
            keys += 1         # one more key is found
            if keys == 64:    # bail on 64th key
                print()
                return index  # index of 64th key

        if not (index & 0xFF):
            print(str(index), end='\r')

real = 'jlmsuwbz'
assert(run('abc') == 22728)
print('Part 1:', run(real))  # 35186
assert(run('abc', p2=True) == 22551)
print('Part 2:', run(real, p2=True))  # 22429
