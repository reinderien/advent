#!/usr/bin/env python3

containers = sorted((int(l) for l in open('17.in').readlines()), reverse=True)


def recurse_p1(index=0, used=0):
    if used == 150: return 1
    if used > 150 or index >= len(containers): return 0
    return (recurse_p1(index=index + 1, used=used + containers[index]) +
            recurse_p1(index=index + 1, used=used))


def dump(ids):
    print(' '.join('%d-%d' % (containers[i], i) for i in ids))


def recurse_p2(index=0, used=0, n_containers=0, min_containers=float('inf'), n_found=0, ids=list()):
    if used == 150:
        if min_containers > n_containers:
            dump(ids)
            return n_containers, 1
        if min_containers == n_containers:
            dump(ids)
            return n_containers, n_found + 1
    if used >= 150 or index >= len(containers): return min_containers, n_found

    taken_min_containers, taken_n_found = recurse_p2(
        index=index + 1, min_containers=min_containers, n_found=n_found, n_containers=n_containers + 1,
        used=used + containers[index], ids=ids + [index])
    if min_containers >= taken_min_containers:
        min_containers, n_found = taken_min_containers, taken_n_found
    return recurse_p2(
        index=index + 1, min_containers=min_containers, n_found=n_found, n_containers=n_containers,
        used=used, ids=ids)


print(recurse_p1())  # 4372
print(recurse_p2())  # 4
