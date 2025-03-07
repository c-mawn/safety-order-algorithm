from simplex import SimplexSolver
import numpy as np
from numpy.typing import NDArray
from copy import deepcopy

def branch_and_bound(c: NDArray, A: NDArray, b: NDArray) -> tuple[None|float, None|float]:
    """
    Solves a MILP problem using branch and cut

    Args:
        c (NDArray): List (# vars)
        A (NDArray): Array (# constraints, # vars)
        b (NDArray): List (# constraints)
        ub (float): The upper bound for Z
        lb (float): The lower bound for Z
    """

    # Initialize a queue with the initial relaxed IP problem
    queue: list[SimplexSolver] = [SimplexSolver(c, A, b)]

    # Initialize the return variables with infeasible values
    best_solution: NDArray | None = None
    best_value: float = np.inf
    
    while len(queue) > 0:

        # Solve the next MILP problem
        solver = queue.pop(0)
        solver.solve()

        # If the problem isn't feasible, move on to the next solution
        is_feasible = True
        if not is_feasible:
            continue

        # If the problem returns a lower value than the current best solution, move on to the next solution
        value: float = solver.tableau[-1, -1]
        if value >= best_value:
            continue

        solution = solver.solution_point()

        # If the solution is a valid IP solution (all values of x are integer), it is the current best solution
        all_integer = all([n.is_integer() for n in solution])
        if all_integer:
            best_solution = solution
            best_value = value
            continue
        
        # Otherwise, we have a better value but a non-integer solution, so we need to add a cut

        distance_from_05: list[float] = [abs(n%1 - 0.5) if solver.basic_columns()[i] else 1 for i, n in enumerate(solution)]
        most_infeasible: int = distance_from_05.index(min(distance_from_05))

        row = solver.tableau[np.where(solver.tableau[:, most_infeasible] == 1), :]

        print(f'{row=}')
        print(row-np.floor(row))
        pass

branch_and_bound(np.array([1, 2]), np.array([[1, 5], [2, 1]]), np.array([14, 8]))
