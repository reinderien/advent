#!/usr/bin/env python3


class PermState:
    """
    For kicks. This is a more complex but potentially more efficient impl of the permutation
    function - churn() is O(1) before normalization.
    """
    __slots__ = ('n', 'off', 'vals', 'inds', 'ops', 'states')

    def __init__(self, text, n):
        self.n = n
        self.off = 0
        self.vals = list(range(n))
        self.inds = list(range(n))
        self.ops = tuple(self._parse(line) for line in text.split(','))

        states_seen = {self.val_str}
        self.states = [self.val_str]
        while True:
            self._churn()
            self._normalize()
            state = self.val_str
            if state in states_seen:
                break
            states_seen.add(state)
            self.states.append(state)

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
        self._swap(i1, i2, self.vals[i1], self.vals[i2])

    def _part(self, v1, v2):
        self._swap(self.inds[v1], self.inds[v2], v1, v2)

    def _swap(self, i1, i2, v1, v2):
        self.vals[i1], self.vals[i2] = v2, v1
        self.inds[v1], self.inds[v2] = i2, i1

    def _churn(self):
        for op in self.ops:
            op()

    def _normalize(self):
        self.vals = self.vals[self.off:] + self.vals[:self.off]
        self.inds = [(i+self.n-self.off)%self.n for i in self.inds]
        self.off = 0

    def get(self, ind):
        return self.states[ind % len(self.states)]

    @property
    def val_str(self):
        return ''.join(chr(v+ord('a')) for v in self.vals)


test_state = PermState('s1,x3/4,pe/b', 5)
assert(test_state.get(1) == 'baedc')
with open('16.in') as f:
    real_state = PermState(f.read(), 16)
print('Part 1:', real_state.get(1))  # kgdchlfniambejop
print('Part 2:', real_state.get(1_000_000_000))  # fjpmholcibdgeakn
