from lp_constraint import LPConstraint, ConstraintType
from two_phase_simplex import TwoPhaseSimplex
from simplex import SimplexSolver

n = 3

q = TwoPhaseSimplex.example(n)
q.solve()
print(q.tableau)
print(q.solution_point())

s = SimplexSolver.example(n)
s.solve()
print(s.tableau)
print(s.solution_point())
