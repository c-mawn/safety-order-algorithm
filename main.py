from lp_constraint import LPConstraint, ConstraintType
from two_phase_simplex import TwoPhaseSimplex

c1 = LPConstraint(
    {
        "x_1": -1,
        "x_2": 3,
    },
    ConstraintType.LESS_THAN,
    6,
)
c2 = LPConstraint(
    {
        "x_1": 1,
        "x_2": -3,
    },
    ConstraintType.EQUAL,
    6,
)
c3 = LPConstraint(
    {
        "x_1": 1,
        "x_2": 1,
    },
    ConstraintType.GREATER_THAN,
    1,
)
q = TwoPhaseSimplex(
    {
        "x_1": 6,
        "x_2": 1,
    },
    [c1, c2, c3],
)

q.solve()
