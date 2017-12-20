#!/usr/bin/env python3


class PermState:
    __slots__ = ('n', 'off', 'vals', 'inds', 'ops')

    def __init__(self, text, n):
        self.n = n
        self.off = 0
        self.vals = list(range(n))
        self.inds = list(range(n))
        self.ops = tuple(self._parse(line) for line in text.split(','))

    def _parse(self, line):
        op = line[0]
        if op == 's':
            delta = int(line[1:])
            return lambda: self._spin(delta)
        args = line[1:].split('/')
        if op == 'x':
            i1, i2 = (int(i) for i in args)
            return lambda: self._exch(i1, i2)
        if op == 'p':
            v1, v2 = (ord(i)-ord('a') for i in args)
            return lambda: self._part(v1, v2)
        raise ValueError()

    def _spin(self, delta):
        self.off = (self.off + self.n - delta) % self.n

    def _exch(self, i1, i2):
        i1 = (i1 + self.off) % self.n
        i2 = (i2 + self.off) % self.n
        self.swap(i1, i2, self.vals[i1], self.vals[i2])

    def _part(self, v1, v2):
        self.swap(self.inds[v1], self.inds[v2], v1, v2)

    def swap(self, i1, i2, v1, v2):
        self.vals[i1], self.vals[i2] = v2, v1
        self.inds[v1], self.inds[v2] = i2, i1

    def churn(self):
        for op in self.ops:
            op()

    def normalize(self):
        self.vals = self.vals[self.off:] + self.vals[:self.off]
        self.inds = [(i+self.n-self.off)%self.n for i in self.inds]
        self.off = 0

    @staticmethod
    def to_str(tup):
        return ''.join(chr(v+ord('a')) for v in tup)

    @property
    def val_str(self):
        return PermState.to_str(self.vals)

    @property
    def ind_str(self):
        return PermState.to_str(self.inds)


def p1(text, n):
    state = PermState(text, n)
    state.churn()
    state.normalize()
    return state


def p2(state):
    for _ in range(100):
        state.churn()
        state.normalize()
        print(state.val_str, state.ind_str)

assert(p1('s1,x3/4,pe/b', 5).val_str == 'baedc')
with open('16.in') as f:
    real_state = p1(f.read(), 16)
    print('Part 1:', real_state.val_str)  # kgdchlfniambejop
    p2(real_state)
