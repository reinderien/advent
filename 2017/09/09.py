#!/usr/bin/env python3


def find_any(haystack, needles, start=0):
    matches = ((i, c) for i, c in enumerate(haystack[start:])
               if c in needles)
    index, needle = next(matches, (None, None))
    if index is None:
        return None, None
    return index + start, needle


def run(text):
    score, index, n_groups, level = 0, 0, 0, 0
    group_next = set('{}<')
    garbage_next = set('!>')
    in_garbage = False

    while True:
        searching_for = garbage_next if in_garbage else group_next
        next_index, next_char = find_any(text, searching_for, index)
        if next_index is None:
            return n_groups, score
        index = next_index + 1
        if in_garbage:
            if next_char == '!':
                index += 1
            elif next_char == '>':
                in_garbage = False
        else:
            if next_char == '{':
                n_groups += 1
                level += 1
                score += level
            elif next_char == '}':
                level -= 1
            elif next_char == '<':
                in_garbage = True


test_n_groups, _ = run('{}')
assert(test_n_groups == 1)
test_n_groups, _ = run('{{{}}}')
assert(test_n_groups == 3)
test_n_groups, _ = run('{{},{}}')
assert(test_n_groups == 3)
test_n_groups, _ = run('{{{},{},{{}}}}')
assert(test_n_groups == 6)
test_n_groups, _ = run('{<{},{},{{}}>}')
assert(test_n_groups == 1)
test_n_groups, _ = run('{<a>,<a>,<a>,<a>}')
assert(test_n_groups == 1)
test_n_groups, _ = run('{{<a>},{<a>},{<a>},{<a>}}')
assert(test_n_groups == 5)
test_n_groups, _ = run('{{<!>},{<!>},{<!>},{<a>}}')
assert(test_n_groups == 2)

_, test_score = run('{}')
assert(test_score == 1)
_, test_score = run('{{{}}}')
assert(test_score == 6)
_, test_score = run('{{},{}}')
assert(test_score == 5)
_, test_score = run('{{{},{},{{}}}}')
assert(test_score == 16)
_, test_score = run('{<a>,<a>,<a>,<a>}')
assert(test_score == 1)
_, test_score = run('{{<ab>},{<ab>},{<ab>},{<ab>}}')
assert(test_score == 9)
_, test_score = run('{{<!!>},{<!!>},{<!!>},{<!!>}}')
assert(test_score == 9)
_, test_score = run('{{<a!>},{<a!>},{<a!>},{<ab>}}')
assert(test_score == 3)

with open('09.in') as f:
    print('Part 1: %d groups, %d score' % run(f.read()))  # 12505
