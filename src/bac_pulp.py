from pulp import *
import numpy as np

p = LpProblem()

x = LpVariable('x')
y = LpVariable('y')

p += 1 * x + 2 * y
p += 1 * x + 5 * y <= 14
p += 2 * x + 1 * y <= 8

def branch_and_cut_pulp(problem: LpProblem):
    while True:
        problem.solve()

        if all([variable.value().is_integer() for variable in problem.variables()]): # type: ignore
            break

        problem.

branch_and_cut_pulp(p)