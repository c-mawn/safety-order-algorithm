"""
Linear programming solver via simplex algorithm
"""

import numpy as np
from numpy.typing import NDArray


class SimplexSolver:

    tableau: NDArray

    def __init__(self, c: NDArray, A: NDArray, b: NDArray):
        # Objective function coefficients
        self.c = c
        # Constraint coefficients
        self.A = A
        # Constraint values
        self.b = b

    @staticmethod
    def example(example_number: int):
        """
        Returns a [SimplexSolver] with a sample A, b, and c
        """
        match example_number:
            case 1:
                # In class example
                c = np.array([8, 10, 7])
                A = np.array([[1, 3, 2], [1, 5, 1]])
                b = np.array([10, 8])
            case 2:
                # Homework 1
                c = np.array([1, 2])
                A = np.array([[1, 3], [1, 1]])
                b = np.array([8, 4])
            case 3:
                # No valid solution
                c = np.array([1, 1])
                A = np.array([[1, 1], [-2, -1]])
                b = np.array([2, -5])
            case 4:
                # Unbounded
                c = np.array([3, 2])
                A = np.array([[1, -1]])
                b = np.array([4])
            case _:
                raise ValueError("No example at that number")
        return SimplexSolver(c, A, b)

    def construct_tableau(self):
        """
        Sets `self.tableau` to the initial tableau based on the given A, b, and c
        """
        center = np.vstack((self.A, self.c * -1))
        identity_stack = np.vstack(
            (
                np.eye(self.A.shape[0]),
                np.zeros(self.A.shape[0]),
            )
        )
        b_col = np.vstack((self.b.reshape(self.A.shape[0], 1), 0))
        self.tableau = np.hstack((center, identity_stack, b_col))

    def select_pivot(self) -> tuple[int, int]:
        """
        Returns the pivot point for the current tableau
        """
        pivot_col = np.argmin(self.tableau[-1, :-1])
        pivot_row = np.argmin(self.tableau[:-1, -1] / self.tableau[:-1, pivot_col])
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
            self.tableau[row_idx, :] -= (
                self.tableau[row_idx, pivot_col] * self.tableau[pivot_row, :]
            )

    def solution_point(self) -> NDArray:
        """
        Returns a numpy array containing the values of the variables and slack
        variables. Does so by finding the columns that are all zeros except for
        one 1
        """
        point = np.zeros(self.tableau.shape[1] - 1)
        for col_idx in range(len(point)):
            col = self.tableau[:, col_idx]
            # If column is all zeros except for one 1
            if np.count_nonzero(col) == 1 and sum(col) == 1:
                # Set variable to the value in the rightmost column that corresponds
                # to the position of the 1
                point[col_idx] = self.tableau[:, -1][np.where(col == 1)]
        return point

    def solve(self):
        """
        Solve via the simplex algorithm, pivoting until all values in the
        objective row are non-negative
        """
        self.construct_tableau()
        while not all(self.tableau[-1, : self.A.shape[1]] >= 0):
            pivot = self.select_pivot()
            self.row_reduce_by_pivot(pivot)


s = SimplexSolver.example(1)
s.solve()
print(s.tableau)
print(s.solution_point())
