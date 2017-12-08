#!/usr/bin/env python3

import re


def p1():
    abba = re.compile(r'([^\[\]])([^\[\]])(?!\1)\2\1')
    hyper = re.compile(r'\[[^\[\]]*([^\[\]])([^\[\]])(?!\1)\2\1[^\[\]]*\]')

    def valid(ip):
        return (
            abba.search(ip)
            and not hyper.search(ip))

    # Tests from question
    assert(valid('abba[mnop]qrst'))
    assert(not valid('abcd[bddb]xyyx'))
    assert(not valid('aaaa[qwer]tyui'))
    assert(valid('ioxxoj[asdfgh]zxcvbn'))

    # Addl tests
    assert(valid('ioxxoj[abbbbe]zxcvbn'))

    nvalid = sum(1 for line in open('07.in') if valid(line))
    print(nvalid)  # 115


def p2():
    rex_aba = re.compile(r'(\w)(?!\1)(\w)\1')
    rex_inner = re.compile(r'\[(.+?)\]')
    rex_outer = re.compile(r'[^\[\]]+(?=\[|$)')

    def valid(ip):
        outer = tuple(m[0] for m in rex_outer.finditer(ip))

        for inner in rex_inner.finditer(ip):
            haystack = inner[1]
            while True:  # Loop for overlapping matches
                aba_inner = rex_aba.search(haystack)
                if not aba_inner:
                    break
                bab = aba_inner.expand(r'\2\1\2')
                if any(bab in o for o in outer):
                    return True
                haystack = haystack[aba_inner.start(0)+1:]

        return False

    # Tests from question
    assert(    valid('aba[bab]xyz'))
    assert(not valid('xyx[xyx]xyx'))
    assert(    valid('aaa[kek]eke'))
    assert(    valid('zazbz[bzb]cdb'))

    # Addl tests
    assert(not valid('sss[sss]sss'))
    assert(not valid('[aba]xx[bab]'))
    assert(    valid('abaxx[1]2[3]4[5bab6]'))
    assert(    valid('3[5bab6][1]2[3]4aba'))

    nvalid = sum(1 for line in open('07.in') if valid(line))
    print(nvalid)

p2()  # 231
