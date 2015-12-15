import re
from scipy.optimize import minimize
from unittest import TestCase


class Ingredient:
    def __init__(self, line):
        self.name = line.split(':')[0]
        self.attrs = {m.group(1): int(m.group(2))
                      for m in re.finditer(r' ([^, ]+) ([-\d]+)(,|$)', line)}
        # Keep these in a known order
        self.weights = (self.attrs['capacity'],
                        self.attrs['durability'],
                        self.attrs['flavor'],
                        self.attrs['texture'])

    def __repr__(self):
        return self.name


def solve(ingredients):
    def objective(args):
        product = -1
        # Instead of having the degrees of freedom be the number of ingredients,
        # reduce that by one so that we can use COBYLA without an equality constraint
        x = tuple(args) + (100-sum(args),)
        for i_attr in range(4):
            total = sum(a*i.weights[i_attr] for a, i in zip(x, ingredients))
            product *= max(0, total)
        return product

    # Use inequality constraints instead of bounds for COBYLA
    constraints = [{'type': 'ineq', 'fun': lambda x: x[i]} for i in range(len(ingredients)-1)] + [
                   {'type': 'ineq', 'fun': lambda x: 100-x[i]} for i in range(len(ingredients)-1)]

    # Use COBYLA - constrained optimization by linear approximation, because
    # SLSQP - sequential least-squares programming fails completely
    res = minimize(method='COBYLA', fun=objective, constraints=constraints, options={'disp': True},
                   x0=(100/len(ingredients),)*(len(ingredients)-1))

    xres = tuple(res.x) + (100-sum(res.x),)
    print('%s: %f' % (xres, -res.fun))

    xres = [int(round(x)) for x in res.x]
    f = objective(xres)
    xres += [100-sum(xres)]
    print('%s: %d' % (xres, -f))
    return xres

test_ingredients = (
    Ingredient('Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8'),
    Ingredient('Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3')
)
test = TestCase()
# 62842880
test.assertEqual(solve(test_ingredients), [44, 56])

all_ingredients = tuple(Ingredient(line) for line in open('15.in').readlines())
# 13882464
solve(all_ingredients)
