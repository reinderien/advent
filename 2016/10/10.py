#!/usr/bin/env python3

import re
from functools import reduce
from operator import mul


def run(lines, part1, chip1=None, chip2=None):
    bots = {}
    outputs = {}

    class Container:
        def __init__(self, id):
            self.id = id
            self.chips = set()

        @staticmethod
        def produce(type, id):
            if type == 'bot':
                cls = Bot
            elif type == 'output':
                cls = Output
            else: raise NotImplementedError(type)

            container = cls.lookup.get(id)
            if not container:
                container = cls(id)
                cls.lookup[id] = container
            return container

    class Bot(Container):
        lookup = bots

        def __init__(self, id):
            super().__init__(id)
            self.low_dest, self.hi_dest = None, None

    class Output(Container):
        lookup = outputs

        def __init__(self, id):
            super().__init__(id)

    def parse():
        re_goes = re.compile(r'^value (\d+) goes to bot (\d+)$')
        re_give = re.compile(r'^bot (\d+) gives low to (output|bot) '
                             r'(\d+) and high to (output|bot) (\d+)$')

        for line in lines:
            match = re_goes.match(line)
            if match:
                chip, bot_id = (int(g) for g in match.groups())
                bot = Container.produce('bot', bot_id)
                bot.chips.add(chip)
            else:
                source, low_type, low_id, hi_type, hi_id = re_give.match(line).groups()
                source, low_id, hi_id = int(source), int(low_id), int(hi_id)
                bot = Container.produce('bot', source)
                bot.low_dest = Container.produce(low_type, low_id)
                bot.hi_dest = Container.produce(hi_type, hi_id)
    parse()

    while True:
        source_bots = [b for b in bots.values() if len(b.chips) == 2]
        if not source_bots:
            break
        source_bot = source_bots[0]
        lower_chip, higher_chip = sorted(source_bot.chips)
        source_bot.chips.clear()
        source_bot.low_dest.chips.add(lower_chip)
        source_bot.hi_dest.chips.add(higher_chip)
        if part1 and lower_chip == chip1 and higher_chip == chip2:
            return source_bot.id

    if part1:
        raise ValueError('Could not find the droid you are looking for')
    return reduce(mul,
                  (next(iter(outputs[id].chips)) for id in range(3)),
                  1)


test_text = \
'''value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2'''.split('\n')
assert(run(test_text, True, 2, 5) == 2)

with open('10.in') as f:
    print('Part 1:', run(f, True, 17, 61))  # 141
    f.seek(0)
    print('Part 2:', run(f, False))  # 1209
