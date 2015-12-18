import re


def p1():
    real_sue = {('children', '3'), ('cats', '7'), ('samoyeds', '2'),
                ('pomeranians', '3'), ('akitas', '0'), ('vizslas', '0'),
                ('goldfish', '5'), ('trees', '3'), ('cars', '2'),
                ('perfumes', '1')}
    sues = ({m.groups()[:2]
             for m in re.finditer(r' ([a-z]+): (\d+)(,|$)', line)}
            for line in open('16.in').readlines())
    return next(i for i, sue in enumerate(sues) if sue <= real_sue) + 1


def p2():
    preds = {'children': lambda x: x == 3,
             'cats': lambda x: x > 7,
             'samoyeds': lambda x: x == 2,
             'pomeranians': lambda x: x < 3,
             'akitas': lambda x: x == 0,
             'vizslas': lambda x: x == 0,
             'goldfish': lambda x: x < 5,
             'trees': lambda x: x > 3,
             'cars': lambda x: x == 2,
             'perfumes': lambda x: x == 1}
    sues = ({m.group(1): int(m.group(2))
             for m in re.finditer(r' ([a-z]+): (\d+)(,|$)', line)}
            for line in open('16.in').readlines())
    return next(i for i, sue in enumerate(sues)
                if all(preds[k](v) for k, v in sue.items())) + 1

print(p1())  # 213
print(p2())  # 323
