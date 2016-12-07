#!/usr/bin/env python3

import re
from numpy.linalg import solve
from numpy import array
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


def solve1(ingredients):
    def fill_dof(args):
        return tuple(args) + (100-sum(args),)

    def objective(args):
        product = -1
        # Instead of having the degrees of freedom be the number of ingredients,
        # reduce that by one so that we can use COBYLA without an equality constraint
        x = fill_dof(args)
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

    xres = fill_dof(res.x)
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
print('Test 1 should be 62842880:')
test.assertEqual(solve1(test_ingredients), [44, 56])
print('\nSoln 1 should be 13882464:')
all_ingredients = tuple(Ingredient(line) for line in open('15.in').readlines())
solve1(all_ingredients)
print()

def solve2(ingredients):

    def fill_dof(args, do_round=False):
        """
        Constraints: Each ingredient >= 0   (register as an ineq)
                     Each ingredient <= 100 (register as an ineq)
                     Sum of ingredients is 100 (use to reduce DOF)
                     Total calories is 500 - you can cheat and use a fake inequality, i.e.
                        epsilon - abs(500 - sum(x * cals)) > 0,
                     and that works for the test case but not well enough for the real input.
                     So, also use calorie requirement to reduce DOF.
        """
        a = array([[1, 1],
                   [ingredients[-2].attrs['calories'], ingredients[-1].attrs['calories']]])
        b = [100 - sum(args),
             500 - sum(a*i.attrs['calories'] for a, i in zip(args, ingredients[:-2]))]
        x = solve(a, b)
        if do_round:
            x = (int(round(v)) for v in x)

        return tuple(args) + tuple(x)

    def objective(args, do_round=False, full=False):
        product = -1
        if full: x = args
        else: x = fill_dof(args, do_round)
        for i_attr in range(4):
            total = sum(a*i.weights[i_attr] for a, i in zip(x, ingredients))
            product *= max(0, total)
        return product

    def cals(args):
        return sum(a*i.attrs['calories'] for a, i in zip(args, ingredients))

    # Use inequality constraints instead of bounds for COBYLA
    constraints = [{'type': 'ineq', 'fun': lambda x: x[i]} for i in range(len(ingredients)-2)] + [
                   {'type': 'ineq', 'fun': lambda x: 100-x[i]} for i in range(len(ingredients)-2)]

    # Use COBYLA - constrained optimization by linear approximation, because
    # SLSQP - sequential least-squares programming fails completely
    res = minimize(method='COBYLA', fun=objective, constraints=constraints, options={'disp': True},
                   x0=(100/len(ingredients),)*(len(ingredients)-2))

    xres = fill_dof(res.x)
    print('%s: score=%f cals=%f' % (xres, -res.fun, cals(xres)))

    # Scipy/numpy are dumb and do not support integer linear programming.
    # BUT I CAN BE DUMBER.
    base = [round(x) for x in xres]
    best_score, best_x = 0, None
    for d1 in range(-2,3):
        for d2 in range(-2,3):
            for d3 in range(-2,3):
                b = (base[0]+d1,base[1]+d2,base[2]+d3)
                b = b + (100 - sum(b),)
                if cals(b) != 500: continue
                score = -objective(b, full=True)
                if best_score < score:
                    best_score = score
                    best_x = b
    print('%s: score=%d' % (best_x, best_score))



print('Test 2 should be 57600000:')
#test.assertEqual(solve2(test_ingredients), (40, 60))

print('\nSoln 2 should be 11171160:')
all_ingredients = tuple(Ingredient(line) for line in open('15.in').readlines())
'''
Should be in the neighbourhood of:
(26.371005138101477, 26.795687339254684, 16.658586605456371, 30.174720917187461): score=11249713.830296 cals=500.000000
'''
solve2(all_ingredients)

