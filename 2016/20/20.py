#!/usr/bin/env python3

from bisect import bisect_left


def load(fname):
    starts, ends = None, None

    with open(fname) as f:
        for line in f:
            ip1, ip2 = (int(i) for i in line.split('-', 1))

            if not starts:
                starts = [ip1]
                ends = [ip2]
                continue

            # We need to find an existing range that contains either ip1 or ip2
            # and if such a range does not exist, create it.
            # A binary search can be used to locate the ranges close to the
            # parsed IPs. Use the `bisect` library.

            # s1 indexes starts such that
            # all starts[:s1] < ip1
            # all starts[s1:] >= ip1
            s1 = bisect_left(starts, ip1)
            iter_from = max(0, s1-1)

            to_remove = []
            new_s, new_e = ip1, ip2
            insert_at = None

            for i, (s, e) in enumerate(
                    zip(starts[iter_from:], ends[iter_from:]), iter_from):
                if s > ip2+1:
                    break
                if e < ip1-1:
                    continue
                # Now we need to merge
                if insert_at is None:
                    insert_at = i
                # print("Merging %u-%u and %u-%u" % (s, e, new_s, new_e))
                to_remove.append(i)
                new_s = min(new_s, s)
                new_e = max(new_e, e)

            if insert_at is None:
                insert_at = s1
            else:
                for i in reversed(to_remove):
                    del starts[i]
                    del ends[i]

            starts.insert(insert_at, new_s)
            ends.insert(insert_at, new_e)
            # assert(starts == list(sorted(starts)))
            # assert(ends == list(sorted(ends)))

    return starts, ends


def p1(starts, ends, exp):
    if starts[0] > 0:
        result = 0
    else:
        result = ends[0] + 1

    print('Part 1: %u' % result)
    if exp is not None:
        assert(result == exp)


def p2(starts, ends, exp):
    total = sum(next_start - prev_end - 1
                for prev_end, next_start in zip(
                    [-1] + ends,
                    starts + [0x100000000]
                ))

    print('Part 2: %u' % total)
    if exp is not None:
        assert(total == exp)


def run(title, fname, exp1=None, exp2=None):
    print(title + ':')
    starts, ends = load(fname)
    p1(starts, ends, exp1)
    p2(starts, ends, exp2)


run('Test', 'test_input.txt', 3, 0x100000000 - 8)
run('Real', 'input.txt', 23923783, 125)
