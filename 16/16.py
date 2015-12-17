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


print(p1())  # 213
