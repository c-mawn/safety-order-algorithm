import numpy as np
from numpy.typing import NDArray

# c = np.array([8, 10, 7])
# # fmt: off
# A = np.array([
#     [1, 3, 2],
#     [1, 5, 1]
# ])
# b = np.array([10, 8])

# c = np.array([1, 2])
# # fmt: off
# A = np.array([
#     [1, 3],
#     [1, 1],
# ])
# b = np.array([8, 4])

# no valid solution
# c = np.array([1, 1])
# # fmt: off
# A = np.array([
#     [1, 1],
#     [-2, -1],
# ])
# b = np.array([2, -5])

# unbounded
c = np.array([3, 2])
# fmt: off
A = np.array([
    [1, -1],
])
b = np.array([4])

def construct_tableau(c: NDArray, A: NDArray, b: NDArray) -> NDArray:
    center = np.vstack((A, c * -1))
    # fmt: off
    identity_stack = np.vstack((
        np.eye(A.shape[0]),
        np.zeros(A.shape[0])
    ))
    b_col = np.vstack((b.reshape(A.shape[0], 1), 0))

    return np.hstack((center, identity_stack, b_col))


def select_pivot(tableau: NDArray) -> tuple[int, int]:
    pivot_col = np.argmin(tableau[-1, :-1])
    pivot_row = np.argmin(tableau[:-1, -1] / tableau[:-1, pivot_col])
    return pivot_row, pivot_col


def row_reduce_by_pivot(tableau: NDArray, pivot: tuple[int, int]) -> NDArray:
    tableau_copy = tableau.copy()
    pivot_row, pivot_col = pivot

    # row reduce so pivot = 1
    tableau_copy[pivot_row, :] /= tableau_copy[pivot_row, pivot_col]
    # reduce other rows
    for row_idx in range(tableau_copy.shape[0]):
        if row_idx == pivot_row:
            continue
        tableau_copy[row_idx, :] -= (
            tableau_copy[row_idx, pivot_col] * tableau_copy[pivot_row, :]
        )
    return tableau_copy


def get_solution_point(tableau: NDArray) -> NDArray:
    out = np.zeros(tableau.shape[1] - 1)
    for col_idx in range(len(out)):
        col = tableau[:, col_idx]
        # If column is all zeros except for one 1
        if np.count_nonzero(col) == 1 and sum(col) == 1:
            # Set variable to the value in the rightmost column that corresponds
            # to the position of the 1
            out[col_idx] = tableau[:, -1][np.where(col == 1)]
    return out


def simplex(c: NDArray, A: NDArray, b: NDArray):
    tableau = construct_tableau(c, A, b)
    while not all(tableau[-1, : A.shape[1]] >= 0):
        pivot = select_pivot(tableau)
        tableau = row_reduce_by_pivot(tableau, pivot)
    print(tableau)
    print(get_solution_point(tableau))


simplex(c, A, b)
