#!/usr/bin/env python3


def text_to_bool(txt):
    return tuple(tuple(1 if c=='#' else 0
                       for c in row) for row in txt)


def transforms(src):
    n = len(src)
    fw, bk = range(n), range(n-1,-1,-1)
    for r1 in (fw, bk):
        for r0 in (fw, bk):
            for x_inner in (True, False):
                yield tuple(tuple(1 if src[d1 if x_inner else d0]
                                          [d0 if x_inner else d1]=='#' else 0
                                  for d0 in r0)
                            for d1 in r1)


def get_rules(fname):
    rules = {}
    with open(fname) as f:
        for line in f:
            src, dst = (s.split('/') for s in line.rstrip().split(' => '))
            dst = text_to_bool(dst)
            rules.update({s: dst for s in transforms(src)})
    return rules


def churn(pattern, rules):
    n = len(pattern)
    if not (n & 2):
        chunksz = 2
    elif not (n % 3):
        chunksz = 3
    else:
        raise ValueError('Bad pattern size')

    new_pat = []
    for ymaj in range(n//chunksz):
        new_lines = [[] for _ in range(chunksz+1)]
        for xmaj in range(n//chunksz):
            chunk = tuple(tuple(pattern[ymaj*chunksz + ymin]
                                       [xmaj*chunksz : (xmaj+1)*chunksz])
                          for ymin in range(chunksz))
            new_chunk = rules[chunk]
            for ymin, subline in enumerate(new_chunk):
                new_lines[ymin].extend(subline)
        new_pat.extend(new_lines)
    return new_pat


def run(fname, iters):
    rules = get_rules(fname)
    pattern = text_to_bool(('.#.',
                            '..#',
                            '###'))
    for _ in range(iters):
        pattern = churn(pattern, rules)

    return sum(sum(c for c in row) for row in pattern)


assert(run('21.test.in', 2) == 12)
print('Part 1:', run('21.in', 5))  # 124 is too low
