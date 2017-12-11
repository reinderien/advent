#!/usr/bin/env python3


def find_any(haystack, needles, start=0):
    matches = ((i, c) for i, c in enumerate(haystack[start:])
               if c in needles)
    index, needle = next(matches, (None, None))
    if index is None:
        return None, None
    return index + start, needle


def run(text):
    score, index, n_groups, level, n_garbage, garbage_start = (0,)*6
    group_next = set('{}<')
    garbage_next = set('!>')
    in_garbage = False

    while True:
        searching_for = garbage_next if in_garbage else group_next
        next_index, next_char = find_any(text, searching_for, index)
        if next_index is None:
            return n_groups, score, n_garbage
        index = next_index + 1
        if in_garbage:
            if next_char == '!':
                index += 1
                garbage_start += 2
            elif next_char == '>':
                in_garbage = False
                n_garbage += index - garbage_start - 1
        else:
            if next_char == '{':
                n_groups += 1
                level += 1
                score += level
            elif next_char == '}':
                level -= 1
            elif next_char == '<':
                in_garbage = True
                garbage_start = index


test_n_groups, _, _ = run('{}')
assert(test_n_groups == 1)
test_n_groups, _, _ = run('{{{}}}')
assert(test_n_groups == 3)
test_n_groups, _, _ = run('{{},{}}')
assert(test_n_groups == 3)
test_n_groups, _, _ = run('{{{},{},{{}}}}')
assert(test_n_groups == 6)
test_n_groups, _, _ = run('{<{},{},{{}}>}')
assert(test_n_groups == 1)
test_n_groups, _, _ = run('{<a>,<a>,<a>,<a>}')
assert(test_n_groups == 1)
test_n_groups, _, _ = run('{{<a>},{<a>},{<a>},{<a>}}')
assert(test_n_groups == 5)
test_n_groups, _, _ = run('{{<!>},{<!>},{<!>},{<a>}}')
assert(test_n_groups == 2)

_, test_score, _ = run('{}')
assert(test_score == 1)
_, test_score, _ = run('{{{}}}')
assert(test_score == 6)
_, test_score, _ = run('{{},{}}')
assert(test_score == 5)
_, test_score, _ = run('{{{},{},{{}}}}')
assert(test_score == 16)
_, test_score, _ = run('{<a>,<a>,<a>,<a>}')
assert(test_score == 1)
_, test_score, _ = run('{{<ab>},{<ab>},{<ab>},{<ab>}}')
assert(test_score == 9)
_, test_score, _ = run('{{<!!>},{<!!>},{<!!>},{<!!>}}')
assert(test_score == 9)
_, test_score, _ = run('{{<a!>},{<a!>},{<a!>},{<ab>}}')
assert(test_score == 3)

with open('09.in') as f:
    print('%d groups, %d score, %d garbage' % run(f.read()))  # P1: 12505  P2: 6671
