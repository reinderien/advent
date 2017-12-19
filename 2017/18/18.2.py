#!/usr/bin/env python3

from collections import deque


class Program:
    def __init__(self, pid, ops):
        self.pid, self.ops = pid, ops
        self.pc, self.n_sent = 0, 0
        self.regs = {'p': pid}
        self.send_queue = deque()
        self.other = None

    def _maybe_reg(self, name):
        if isinstance(name, int):
            return name
        return self.regs.get(name, 0)

    def step(self):
        """
        :return: True if program is terminated or blocked
        """
        if not (0 <= self.pc < len(self.ops)):
            return True
        op = self.ops[self.pc]
        if op[0] == 'jgz':
            test = self._maybe_reg(op[1])
            if test > 0:
                self.pc += self._maybe_reg(op[2])
            else:
                self.pc += 1
        else:
            if op[0] == 'snd':
                self.send_queue.append(self._maybe_reg(op[1]))
                self.n_sent += 1
            elif op[0] == 'set':
                self.regs[op[1]] = self._maybe_reg(op[2])
            elif op[0] == 'add':
                self.regs[op[1]] = self.regs.setdefault(op[1], 0) + self._maybe_reg(op[2])
            elif op[0] == 'mul':
                self.regs[op[1]] = self.regs.setdefault(op[1], 0) * self._maybe_reg(op[2])
            elif op[0] == 'mod':
                self.regs[op[1]] = self.regs.setdefault(op[1], 0) % self._maybe_reg(op[2])
            elif op[0] == 'rcv':
                if self.other.send_queue:
                    self.regs[op[1]] = self.other.send_queue.popleft()
                else:
                    return True
            self.pc += 1
        return False


def run(fname):
    with open(fname) as f:
        ops = tuple(line.rstrip().split(' ') for line in f)
    for op in ops:
        for i,v in enumerate(op):
            try:
                op[i] = int(v)
            except ValueError:
                pass

    p0, p1 = Program(0, ops), Program(1, ops)
    p0.other, p1.other = p1, p0

    while not (p0.step() and p1.step()):
        pass
    return p1.n_sent

print('Part 2:', run('18.in'))  # 7366
