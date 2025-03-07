import numpy as np
from numpy.typing import NDArray
from enum import Enum
from typing import Dict, List
from simplex import SimplexSolver


class ConstraintType(Enum):
    LESS_THAN = 0
    EQUAL = 1
    GREATER_THAN = 2


class LPConstraint:
    """
    Example: 2x + 3y <= 5
        coef_map = {x: 2, y: 3}
        ctype = LESS_THAN
        rhs = 5
    """

    def __init__(self, coef_map: Dict[str, int], ctype: ConstraintType, rhs: float):
        self.coef_map = coef_map
        self.ctype = ctype
        self.rhs = rhs

    def __repr__(self):
        match self.ctype:
            case ConstraintType.LESS_THAN:
                operator = "<="
            case ConstraintType.GREATER_THAN:
                operator = ">="
            case ConstraintType.EQUAL:
                operator = "=="
        return (
            " + ".join([f"{coef}{var}" for var, coef in self.coef_map.items()])
            + f" {operator} {str(self.rhs)}"
        )

    def convert_to_standard_form(self, constraint_idx: int):
        match self.ctype:
            case ConstraintType.LESS_THAN:
                # Add slack variable
                self.coef_map[f"s_{constraint_idx}"] = 1
            case ConstraintType.GREATER_THAN:
                # Subtract slack variable and add artificial variable
                self.coef_map[f"s_{constraint_idx}"] = -1
                self.coef_map[f"a_{constraint_idx}"] = 1
            case ConstraintType.EQUAL:
                # Add artificial variable
                self.coef_map[f"a_{constraint_idx}"] = 1
        self.ctype = ConstraintType.EQUAL


class TwoPhaseSimplex:
    def __init__(self, objective: Dict[str, int], constraints: List[LPConstraint]):
        self.objective = objective
        self.constraints = constraints

    def construct_tableau(self):
        variables = set()
        # Convert all to standard form, collect variables (including slack and artificial)
        for idx, constraint in enumerate(self.constraints):
            constraint.convert_to_standard_form(idx + 1)
            variables.update(constraint.coef_map.keys())

        # Init variable column map with sorted variables
        variable_column_map = {}
        artificial_variables = [var for var in variables if var.startswith("a")]

        def variable_sort(var: str):
            match var[0]:
                case "a":
                    return (2, var)
                case "s":
                    return (1, var)
                case _:
                    return (0, var)

        for idx, var in enumerate(sorted(variables, key=variable_sort)):
            variable_column_map[var] = idx

        # Construct tableau (assume there are artificial variables)
        tableau: NDArray = None

        for constraint in self.constraints:
            # Construct constraint row
            row = np.zeros(len(variable_column_map) + 1)
            for var, coef in constraint.coef_map.items():
                row[variable_column_map[var]] = coef
            row[-1] = constraint.rhs

            # Add row to tableau
            if tableau is None:
                tableau = row
            else:
                tableau = np.vstack((tableau, row))

        # Add objective function as last row
        obj_row = np.zeros(len(variable_column_map) + 1)
        for var in artificial_variables:
            obj_row[variable_column_map[var]] = 1
        tableau = np.vstack((tableau, obj_row))

        print(tableau)

        # Subtract rows that contain artificial variables from the objective row
        # to make artificial variables basic
        for var in artificial_variables:
            artificial_col = variable_column_map[var]
            artificial_row = np.where(tableau[:, artificial_col] == 1)[0][0]
            tableau[-1, :] -= tableau[-1, artificial_col] * tableau[artificial_row, :]

        print(tableau)
        return tableau


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

# q.construct_tableau()

p = SimplexSolver.example(1)
p.tableau = q.construct_tableau()
# while not all(p.tableau[-1, : p.A.shape[1]] >= 0):
for _ in range(1):
    pivot = p.select_pivot()
    p.row_reduce_by_pivot(pivot)
    print(p.tableau)
    print("----")
