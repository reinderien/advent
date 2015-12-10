#!/usr/bin/env python3

from re import match

nodes = {}


class Node:
    def __init__(self, name):
        self.name, self.links, self.used = name, set(), False

    def recurse(self, so_far=0, cap=float('inf')):
        self.used = True
        try:
            avail_links = {l for l in self.links if not l.other(self).used}
            if not avail_links: return so_far, self.name
            best_dist, best_seq = float('inf'), ''
            for link in avail_links:
                next_so_far = so_far + link.dist
                if next_so_far >= cap: continue
                dist, seq = link.other(self).recurse(
                    cap=min(cap, best_dist),
                    so_far=next_so_far)
                if best_dist > dist: best_dist, best_seq = dist, seq
            return best_dist, '%s - %s' % (self.name, best_seq)
        finally: self.used = False


class Link:
    def __init__(self, a, b, dist):
        self.dist = int(dist)
        self.a = nodes.setdefault(a, Node(a))
        self.b = nodes.setdefault(b, Node(b))
        self.a.links.add(self)
        self.b.links.add(self)

    def other(self, n):
        return self.a if self.b is n else self.b

for line in open('9.in').readlines():
    Link(*match(r'^(.+) to (.+) = (.+)$', line).groups())

top_min_dist, top_min_seq = float('inf'), ''
for start_node in nodes.values():
    top_dist, top_seq = start_node.recurse(cap=top_min_dist)
    if top_min_dist > top_dist: top_min_dist, top_min_seq = top_dist, top_seq

# 117: Faerun - AlphaCentauri - Tambi - Snowdin - Norrath - Tristram - Arbre - Straylight
print('%d: %s' % (top_min_dist, top_min_seq))
