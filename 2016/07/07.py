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
    print(nvalid)


def p2():
    first = r'(\w)(?!\1)(\w)\1'
    others = r'(\w*\[\w*\]\w*)*'
    second = r'\2\1\2'
    openb = r'\[\w*'
    closeb = r'\w*\]'
    patl = re.compile(first + others + openb + second + closeb)
    patr = re.compile(openb + first + closeb + others + second)
    def valid(ip):
        return any(p.search(ip) for p in (patl, patr))

    # Tests from question
    assert(    valid('aba[bab]xyz'))
    assert(not valid('xyx[xyx]xyx'))
    assert(    valid('aaa[kek]eke'))
    assert(    valid('zazbz[bzb]cdb'))

    # Addl tests
    assert(not valid('[aba]xx[bab]'))
    assert(    valid('abaxx[1]2[3]4[5bab6]'))
    assert(    valid('3[5bab6][1]2[3]4aba'))

    nvalid = sum(1 for line in open('07.in') if valid(line))
    print(nvalid)

p2()  # 39, 82, 153 too low
