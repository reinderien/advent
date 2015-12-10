#!/usr/bin/env python3

from re import match

all_links, nodes = [], {}


class Node:
    def __init__(self, name):
        self.name, self.links = name, set()

    def recurse(self, so_far=0, bound=0, avail_links=all_links, depth=0):
        if not avail_links: return so_far, self.name

        n_remain = len(nodes)-depth-1
        highest_possible = so_far + sum(l.dist for l in avail_links[:n_remain])
        if highest_possible <= bound: return 0, ''

        new_avail_links = [l for l in avail_links if self not in (l.a,l.b)]
        neighbour_links = [l for l in avail_links if self in (l.a, l.b)]
        best_dist, best_seq = 0, ''
        for link in neighbour_links:
            next_so_far = so_far + link.dist
            dist, seq = link.other(self).recurse(
                bound=max(bound, best_dist),
                so_far=next_so_far,
                avail_links=new_avail_links,
                depth=depth+1)
            if best_dist < dist: best_dist, best_seq = dist, seq
        return best_dist, '%s - %s' % (self.name, best_seq)


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
    all_links.append(Link(*match(r'^(.+) to (.+) = (.+)$', line).groups()))
all_links.sort(key=lambda l: -l.dist)

top_max_dist, top_max_seq = 0, ''
for start_node in nodes.values():
    top_dist, top_seq = start_node.recurse(bound=top_max_dist)
    if top_max_dist < top_dist: top_max_dist, top_max_seq = top_dist, top_seq

# 909: Tambi - Arbre - Faerun - Norrath - AlphaCentauri - Straylight - Tristram - Snowdin
print('%d: %s' % (top_max_dist, top_max_seq))
