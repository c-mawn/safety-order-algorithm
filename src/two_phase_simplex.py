import numpy as np
from numpy.typing import NDArray
from typing import Dict, List
from lp_constraint import LPConstraint, ConstraintType


class TwoPhaseSimplex:
    def __init__(self, objective: Dict[str, int], constraints: List[LPConstraint]):
        self.objective = objective
        self.constraints = constraints

        self.tableau: NDArray = None
        self.variable_column_map: Dict[str, int] = {}
        self.has_artificial_variables = False

    @staticmethod
    def example(example_number: int):
        match example_number:
            case 1:
                # In class example
                return TwoPhaseSimplex(
                    {"x1": 8, "x2": 10, "x3": 7},
                    [
                        LPConstraint(
                            {"x1": 1, "x2": 3, "x3": 2},
                            ConstraintType.LESS_THAN,
                            10,
                        ),
                        LPConstraint(
                            {"x1": 1, "x2": 5, "x3": 1},
                            ConstraintType.LESS_THAN,
                            8,
                        ),
                    ],
                )
            case 2:
                # Homework 1
                return TwoPhaseSimplex(
                    {"x1": 1, "x2": 2},
                    [
                        LPConstraint({"x1": 1, "x2": 3}, ConstraintType.LESS_THAN, 8),
                        LPConstraint({"x1": 1, "x2": 1}, ConstraintType.LESS_THAN, 4),
                    ],
                )
            case 3:
                # No valid solution
                return TwoPhaseSimplex(
                    {"x1": 1, "x2": 1},
                    [
                        LPConstraint(
                            {"x1": 1, "x2": 1}, ConstraintType.GREATER_THAN, 5
                        ),
                        LPConstraint({"x1": 1, "x2": 1}, ConstraintType.LESS_THAN, 2),
                    ],
                )
            case 4:
                # Unbounded
                return TwoPhaseSimplex(
                    {"x1": 3, "x2": 2},
                    [
                        LPConstraint({"x1": 1, "x2": -1}, ConstraintType.LESS_THAN, 4),
                    ],
                )
            case 5:
                # Binary example, Maya Backpack
                return TwoPhaseSimplex(
                    {"x1": 6, "x2": 12, "x3": 4, "x4": 8, "x5": 10},
                    [
                        LPConstraint(
                            {"x1": 2, "x2": 4, "x3": 10, "x4": 5, "x5": 9},
                            ConstraintType.LESS_THAN,
                            15,
                        ),
                        LPConstraint({"x1": 1}, ConstraintType.LESS_THAN, 1),
                        LPConstraint({"x2": 1}, ConstraintType.LESS_THAN, 1),
                        LPConstraint({"x3": 1}, ConstraintType.LESS_THAN, 1),
                        LPConstraint({"x4": 1}, ConstraintType.LESS_THAN, 1),
                        LPConstraint({"x5": 1}, ConstraintType.LESS_THAN, 1),
                    ],
                )

    # ============================ Initialization ============================
    # region Initialization

    def standardize_constraints(self):
        # Convert all to standard form
        for idx, constraint in enumerate(self.constraints):
            constraint.convert_to_standard_form(idx + 1)

    def init_variable_column_map(self):
        # Init variable column map with sorted variables
        def variable_sort(var: str):
            if var.startswith(LPConstraint.ARTIFICIAL_VAR_TAG):
                return (2, var)
            elif var.startswith(LPConstraint.SLACK_VAR_TAG):
                return (1, var)
            else:
                return (0, var)

        variables = set()
        # Collect variables (including slack and artificial)
        for constraint in self.constraints:
            variables.update(constraint.coef_map.keys())

        # Sort and insert into variable column map
        for idx, var in enumerate(sorted(variables, key=variable_sort)):
            # Check for artificial variables
            if (
                var.startswith(LPConstraint.ARTIFICIAL_VAR_TAG)
                and not self.has_artificial_variables
            ):
                self.has_artificial_variables = True
            self.variable_column_map[var] = idx

    # endregion

    # ========================= Tableau Construction =========================
    # region Tableau Construction

    def add_constraints_to_tableau(self):
        """
        Converts constraints to matrix form and adds them to the tableau.
        This initiates the tableau, should be called before adding objective
        function.
        """
        tableau: NDArray = None
        for constraint in self.constraints:
            # Construct constraint row
            row = np.zeros(len(self.variable_column_map) + 1)
            for var, coef in constraint.coef_map.items():
                row[self.variable_column_map[var]] = coef
            row[-1] = constraint.rhs

            # Add row to tableau
            if tableau is None:
                tableau = row
            else:
                tableau = np.vstack((tableau, row))
        self.tableau = tableau

    def add_two_phase_objective(self):
        """
        Used if there are artificial variables in the tableau. The objective
        of the first phase is to minimize the sum of artificial variables.
        """
        artificial_variables = [
            var
            for var in self.variable_column_map.keys()
            if var.startswith(LPConstraint.ARTIFICIAL_VAR_TAG)
        ]

        # Add objective function as last row, objective function is artificial
        # variables as 1s
        obj_row = np.zeros(len(self.variable_column_map) + 1)
        for var in artificial_variables:
            obj_row[self.variable_column_map[var]] = 1
        self.tableau = np.vstack((self.tableau, obj_row))

        # Subtract rows that contain artificial variables from the objective row
        # to make artificial variables basic
        for var in artificial_variables:
            artificial_col = self.variable_column_map[var]
            artificial_row = np.where(self.tableau[:, artificial_col] == 1)[0][0]
            self.row_elimination(-1, artificial_row, artificial_col)

    def add_single_phase_objective(self):
        obj_row = np.zeros(len(self.variable_column_map) + 1)
        for var, coef in self.objective.items():
            obj_row[self.variable_column_map[var]] = -coef
        self.tableau = np.vstack((self.tableau, obj_row))

    def construct_tableau(self):
        # Construct tableau
        self.add_constraints_to_tableau()
        if self.has_artificial_variables:
            # If there are artificial variables, two phase
            self.add_two_phase_objective()
        else:
            # If no artificial variables, single phase
            self.add_single_phase_objective()

    # endregion

    # =============================== Pivoting ===============================
    # region Pivoting

    def select_pivot(self) -> tuple[int, int]:
        """
        Returns the pivot point for the current tableau
        """
        pivot_col = np.argmin(self.tableau[-1, :-1])

        # Value greater than zero with the smallest ratio selected as pivot
        ratio_col = self.tableau[:-1, -1] / self.tableau[:-1, pivot_col]
        feasible_pivots = ratio_col[ratio_col > 0]
        if len(feasible_pivots) == 0:
            raise ValueError("No feasible pivots")
        pivot_row = np.where(ratio_col == min(feasible_pivots))[0][0]
        return pivot_row, pivot_col

    def row_reduce_by_pivot(self, pivot: tuple[int, int]) -> NDArray:
        """
        Updates the current tableau via row reduction, reducing the pivot row
        such that the pivot is equal to 1, and reducing other rows such that
        the value in the pivot column is 0
        """
        pivot_row, pivot_col = pivot

        # row reduce so pivot = 1
        self.tableau[pivot_row, :] /= self.tableau[pivot_row, pivot_col]
        # reduce other rows
        for row_idx in range(self.tableau.shape[0]):
            if row_idx == pivot_row:
                continue
            self.row_elimination(row_idx, pivot_row, pivot_col)

    def row_elimination(self, active_row: int, pivot_row: int, pivot_col: int):
        """
        Subtract the pivot row from the active row such that the value in the
        pivot column is 0
        """
        self.tableau[active_row, :] -= (
            self.tableau[active_row, pivot_col] * self.tableau[pivot_row, :]
        )

    # endregion

    # ================================ Helpers ================================
    # region Helpers

    def column_is_basic(self, col_idx: int) -> bool:
        col = self.tableau[:, col_idx]
        return np.count_nonzero(col) == 1 and sum(col) == 1

    def has_basic_artificial_variable(self) -> bool:
        for var in self.variable_column_map.keys():
            if var.startswith(LPConstraint.ARTIFICIAL_VAR_TAG) and self.column_is_basic(
                self.variable_column_map[var]
            ):
                return True
        return False

    def decision_vars(self) -> List[str]:
        return [
            var
            for var in self.variable_column_map.keys()
            if not var.startswith(
                (LPConstraint.ARTIFICIAL_VAR_TAG, LPConstraint.SLACK_VAR_TAG)
            )
        ]

    # endregion

    # ================================= Solve =================================
    # region Solve

    def update_tableau_for_second_phase(self):
        # Delete artificial columns
        artificial_cols = [
            self.variable_column_map[var]
            for var in self.variable_column_map.keys()
            if var.startswith(LPConstraint.ARTIFICIAL_VAR_TAG)
        ]
        self.tableau = np.delete(self.tableau, artificial_cols, axis=1)

        # Change objective function
        debasiced_cols = []
        for var, coef in self.objective.items():
            col_idx = self.variable_column_map[var]
            if self.column_is_basic(col_idx):
                debasiced_cols.append(col_idx)
            self.tableau[-1, col_idx] = -coef  # NEGATIVE

        # Re-basic variables that got messed up by adding the objective function
        for col_idx in debasiced_cols:
            row_idx = np.where(self.tableau[:, col_idx] == 1)[0][0]
            self.row_elimination(-1, row_idx, col_idx)

    def solve_single_phase(self):
        # Count of non-slack variables, there should be no artificial variables
        # at this point
        num_decision_vars = len(self.decision_vars())
        while not all(self.tableau[-1, :num_decision_vars] >= 0):
            pivot = self.select_pivot()
            self.row_reduce_by_pivot(pivot)

    def solve_two_phase(self):
        while self.has_basic_artificial_variable():
            pivot = self.select_pivot()
            self.row_reduce_by_pivot(pivot)
            if all(self.tableau[-1, :-1] >= 0):
                # If bottom row values are all non-negative and artificial
                # variables are still basic, the solution is infeasible
                raise ValueError("Infeasible solution")

        self.update_tableau_for_second_phase()
        self.solve_single_phase()

    def solve(self):
        self.standardize_constraints()
        self.init_variable_column_map()
        self.construct_tableau()
        if self.has_artificial_variables:
            self.solve_two_phase()
        else:
            self.solve_single_phase()

    # endregion

    # ================================= Results =================================
    # region Results

    def solution_point(self) -> NDArray:
        num_decision_vars = len(self.decision_vars())
        point = np.zeros(num_decision_vars)
        for col_idx in range(num_decision_vars):
            col = self.tableau[:, col_idx]
            # If column is all zeros except for one 1
            if self.column_is_basic(col_idx):
                # Set variable to the value in the rightmost column that corresponds
                # to the position of the 1
                point[col_idx] = self.tableau[:, -1][np.where(col == 1)]
        return point

    # endregion
