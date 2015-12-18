#!/usr/bin/env python3

import re
from unittest import TestCase


class Reindeer:
    line_format = re.compile(
        r'^(.+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')

    def __init__(self, line):
        self.name, speed, fly_time, rest_time = self.line_format.match(line).groups()
        self.speed, self.fly_time, self.rest_time = int(speed), int(fly_time), int(rest_time)

    def __repr__(self):
        return self.name

    def dist(self, time):
        full_periods, partial_time = divmod(time, self.fly_time + self.rest_time)
        return self.speed * (full_periods * self.fly_time + min(self.fly_time, partial_time))


# Test cases from part 1 description
d1 = Reindeer('Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.')
d2 = Reindeer('Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.')
test = TestCase()
test.assertEqual(14, d1.dist(1))
test.assertEqual(16, d2.dist(1))
test.assertEqual(140, d1.dist(10))
test.assertEqual(160, d2.dist(10))
test.assertEqual(140, d1.dist(11))
test.assertEqual(176, d2.dist(11))
test.assertEqual(140, d1.dist(12))
test.assertEqual(176, d2.dist(12))
test.assertEqual(1120, d1.dist(1000))
test.assertEqual(1056, d2.dist(1000))

all_deers = {Reindeer(line) for line in open('14.in').readlines()}
total_time = 2503

# 2640
print(max(d.dist(total_time) for d in all_deers))


def points(deers, time):
    scores = {d.name: 0 for d in deers}
    for t in range(time):
        dists = {deer.name: deer.dist(t + 1) for deer in deers}
        best_dist = max(d for d in dists.values())
        for name in (n for n, d in dists.items() if d == best_dist):
            scores[name] += 1
    return scores


# Test cases from part 2 description
test_deers = {d1, d2}
p = points(test_deers, 1)
test.assertEqual(1, p['Dancer'])
test.assertEqual(0, p['Comet'])
p = points(test_deers, 140)
test.assertEqual(1, p['Comet'])
test.assertEqual(139, p['Dancer'])
p = points(test_deers, 1000)
test.assertEqual(689, p['Dancer'])
test.assertEqual(312, p['Comet'])

# 1102
print(max(p for p in points(all_deers, total_time).values()))
