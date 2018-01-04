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


def churn(old_pat, rules):
    old_n = len(old_pat)
    if not (old_n % 2):
        old_chunk_sz, new_chunk_sz = 2, 3
    elif not (old_n % 3):
        old_chunk_sz, new_chunk_sz = 3, 4
    else:
        raise ValueError('Bad pattern size')
    new_n = old_n*new_chunk_sz // old_chunk_sz

    new_pat = [[] for _ in range(new_n)]
    for ymaj in range(old_n//old_chunk_sz):
        for xmaj in range(old_n//old_chunk_sz):
            old_chunk = tuple(tuple(old_pat[ymaj*old_chunk_sz + ymin]
                                           [xmaj*old_chunk_sz : (xmaj+1)*old_chunk_sz])
                              for ymin in range(old_chunk_sz))
            for ymin, subline in enumerate(rules[old_chunk]):
                new_pat[ymaj*new_chunk_sz + ymin].extend(subline)
    return new_pat


def run(fname, iters):
    rules = get_rules(fname)
    pattern = text_to_bool(('.#.',
                            '..#',
                            '###'))
    for _ in range(iters):
        pattern = churn(pattern, rules)
    return sum(sum(row) for row in pattern)


assert(run('21.test.in', 2) == 12)
print('Part 1:', run('21.in',  5))  # 142
print('Part 2:', run('21.in', 18))  # 1879071
