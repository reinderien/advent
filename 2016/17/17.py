#!/usr/bin/env python3

from collections import deque, namedtuple
from hashlib import md5


dirns = ((b'U',  0, -1),
         (b'D',  0,  1),
         (b'L', -1,  0),
         (b'R',  1,  0))

Node = namedtuple('Node', ('letter', 'x', 'y'))
Path = namedtuple('Path', ('nodes', 'hash'))


def path_to_str(path):
    return ''.join(p.letter.decode() for p in path.nodes)


def grow_path(path, xdel, ydel, dirn, hexit):
    last = path.nodes[-1]
    x, y = last.x + xdel, last.y + ydel
    if not (0 <= x < 4 and 0 <= y < 4 and
            hexit >= 'b'):
        return None

    new_hash = path.hash.copy()
    new_hash.update(dirn)
    return Path(nodes=path.nodes + [Node(dirn, x, y)], hash=new_hash)


def run(pwd, expected=None):
    root_hash = md5()
    root_hash.update(pwd.encode())
    start = Path(nodes=[Node(b'', 0, 0)], hash=root_hash)
    frontier = deque()
    frontier.append(start)

    while True:
        path = frontier.popleft()
        last = path.nodes[-1]
        if (last.x, last.y) == (3, 3):
            break

        hexits = path.hash.hexdigest()[:4]
        for (dirn, xdel, ydel), hexit in zip(dirns, hexits):
            new_path = grow_path(path, xdel, ydel, dirn, hexit)
            if new_path is not None:
                frontier.append(new_path)

    path = path_to_str(path)
    print('%s -> %s' % (pwd, path))
    if expected is not None and expected != path:
        print('%s != %s' % (path, expected))
        raise AssertionError('Unexpected output')


try:
    run('hijkl')
    raise AssertionError('This password should not work')
except IndexError:
    pass

run('ihgpwlah', 'DDRRRD')
run('kglvqrro', 'DDUDRLRRUDRD')
run('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')
run('pxxbnzuo')
