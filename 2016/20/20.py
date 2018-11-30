#!/usr/bin/env python3

from bisect import bisect_left


def run(fname):
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

            to_remove = []
            new_s, new_e = ip1, ip2
            insert_at = None

            for i, (s, e) in enumerate(
                    zip(starts[s1:], ends[s1:]), s1):
                if s > ip2+1:
                    break
                if e < ip1-1:
                    continue
                # Now we need to merge
                if insert_at is None:
                    insert_at = i
                print("Merging %u-%u and %u-%u" % (s, e, new_s, new_e))
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

    if starts[0] > 0:
        return 0
    return ends[0] + 1


assert(run('test_input.txt') == 3)
print(run('input.txt'))  # 166476 is too low
