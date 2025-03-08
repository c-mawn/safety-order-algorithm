# Safety Order Algorithm

_Ian Lum, Charlie Mawn, Dominic Salmieri_

## Background

### Simplex

The Simplex is an algorithm used for linear programming—the optimization of an objective function given various inequality constraints. Simplex is the most common algorithm for linear programming, solving problems by moving from vertex to vertex in the solution space. The algorithm was invented by George Dantzig, a US Army Air Force logistics planner, in 1946. Dantzig formulated his problems as linear inequalities, then realized the importance of introducing an objective function, adding the notion of a best solution amongst the many feasible solutions.

## How it works

### Simplex

The Simplex algorithm finds the maximum value of a linear objective function given any number of linear constraints. For example:

$$ \text{Maximize: } Z = 2x_1 + x_2 $$

Subject to:

$$ x_1 + 2x_2 \leq 5 $$
$$ x_1 + x_2 \geq 3 $$
$$ x_1 - x_2 = 2 $$

Simplex does so by:

1. Converting the constraints into standard form
2. Converting to a **tableau** matrix
3. Performing an initial phase to remove artificial variables
4. Performing a second phase of traversing vertices by performing matrix row operations, eventually reaching the optimal solution

#### Standard Form

**Note: Simplex assumes all variables are non-negative.**

The first step of the Simplex algorithm is to rewrite constraints in standard form. Standard form means that inequalities are turned into equal signs by adding **slack variables**. Slack variables represent the amount that the LHS of an inequality is off from the RHS.

Take the following constraints for example:

$$ x_1 + 2x_2 \leq 5 $$
$$ x_1 + x_2 \geq 3 $$
$$ x_1 - x_2 = 2 $$

Adding slack variables to turn the inequalities into equalities:

$$ x_1 + 2x_2 + s_1 = 5 $$
$$ x_1 + x_2 - s_2 = 3 $$
$$ x_1 - x_2 = 2 $$

_Because all variables, including slack variables are non-negative, for there to a feasible answer to $` x_1 + 2x_2 + s_1 = 5 `$, the inequality $` x_1 + 2x_2 \leq 5 `$ will be satisfied._

Then, each equation needs to have a **basic** variable. Basic variables are variables that have a coefficient of positive one, not including the original variables that are being optimized. For $\leq$ equations, the slack variable serves this purpose but for = and $\geq$ equations, we add **artificial variables**.

Adding artificial variables to the equations:

$$ x_1 + x_2 - s_2 + a_2 = 3 $$
$$ x_1 - x_2 + a_3 = 2 $$

_The equation $` x_1 + 2x_2 + s_1 = 5 `$ does not need an artificial variable as it already has a basic variable, $`s_1`$._

#### Tableau

The tableau is a matrix representation of the standard form equations. The tableau has an additional step if there are artificial variables, so an example without artificial variables will be shown first.

##### No Artificial Variables

Given the following problem:

$$ \text{Maximize: } Z = 2x_1 + x_2 $$

Subject to:

$$ x_1 + 2x_2 \leq 5 $$
$$ 4x_1 + x_2 \leq 6 $$

Standard form:

$$ x_1 + 2x_2 + s_1 = 5 $$
$$ 4x_1 + x_2 + s_2 = 6 $$

Each variable is assigned a column in the tableau, with the last column representing the RHS of the equation. The constraints would be represented like so:

| Base | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- |
| s1   | 1   | 2   | 1   | 0   | 5   |
| s2   | 4   | 1   | 0   | 1   | 6   |

The base column represents the **basic variable** of the row. Basic variables can be indentified by the column that has a coefficient of 1, where all other values in said column are 0.

Next, the objective function is added like so:

| Base | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- |
| s1   | 1   | 2   | 1   | 0   | 5   |
| s2   | 4   | 1   | 0   | 1   | 6   |
| Z    | -2  | -1  | 0   | 0   | 0   |

Note that the coefficients of the objective function are negative. This is because the objective function is rewritted so all variables are on the LHS, like so:

$$ Z = 2x_1 + x_2 $$
$$ Z - 2x_1 - x_2 = 0 $$

One can also imagine a $Z$ column like so:

| Base | Z   | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- | --- |
| s1   | 0   | 1   | 2   | 1   | 0   | 5   |
| s2   | 0   | 4   | 1   | 0   | 1   | 6   |
| Z    | 1   | -2  | -1  | 0   | 0   | 0   |

This column will always remain unchanged, but it is helpful for understanding the formation of tableau.

This tableau is now ready to run through the Simplex algorithm, and it can skip phase 1 as there are no artificial variables.

##### With Artificial Variables

Given the following problem:

$$ \text{Maximize: } Z = 2x_1 + x_2 $$

Subject to:

$$ x_1 + 2x_2 \leq 5 $$
$$ x_1 + x_2 \geq 3 $$

Standard form:

$$ x_1 + 2x_2 + s_1 = 5 $$
$$ x_1 + x_2 - s_2 + a_2 = 3 $$

Constraints are inserted into the tableau the same as above:

| Base | x1  | x2  | s1  | s2  | a2  | RHS |
| ---- | --- | --- | --- | --- | --- | --- |
| s1   | 1   | 2   | 1   | 0   | 0   | 5   |
| a2   | 1   | 1   | 0   | -1  | 1   | 3   |

Note that the artificial variable $a_2$ is the basic variable for the second row. If an artificial variable was not added, the second row would have no basic variable.

The first phase of the Simplex algorithm is to remove artificial variables. This is done by setting $Z$ to minimize the sum of the artificial variables:

$$ \text{Minimize: } Z = a_2 $$

This can be rewritten in to the following maximization problem:

$$ \text{Maximize: } Z = -a_2 $$

Bringing all variables to the LHS:

$$ Z + a_2 = 0 $$

Added to the tableau:

| Base | x1  | x2  | s1  | s2  | a2  | RHS |
| ---- | --- | --- | --- | --- | --- | --- |
| s1   | 1   | 2   | 1   | 0   | 0   | 5   |
|      | 1   | 1   | 0   | -1  | 1   | 3   |
| Z    | 0   | 0   | 0   | 0   | 1   | 0   |

However, $`a_2`$ is no longer a basic variable as it has a 1 in the $Z$ row. To reconcile this we perform a row operation, subtracting the second row from the $Z$ row:

| Base | x1  | x2  | s1  | s2  | a2  | RHS |
| ---- | --- | --- | --- | --- | --- | --- |
| s1   | 1   | 2   | 1   | 0   | 0   | 5   |
| a2   | 1   | 1   | 0   | -1  | 1   | 3   |
| Z    | -1  | -1  | 0   | 1   | 0   | 0   |

This tableau is now ready for the first phase.

#### Phase 1

In order to maximize a tableau the following steps are performed:

1. Select the most negative coefficient in the $Z$ row, this is the **pivot column**
2. Calculate the ratio between RHS and the pivot column, by dividing the RHS by the pivot column. The element that results in smallest positive ratio is selected as the **pivot**, and its row is the **pivot row**.
3. Divide the pivot row by the pivot element, so the pivot element is 1.
4. Subtract other rows by the pivot row until all other elements in the pivot column are 0.
5. Repeat until a given stop condition.

For our example:

| Base | x1      | x2  | s1  | s2  | a2  | RHS |
| ---- | ------- | --- | --- | --- | --- | --- |
| s1   | 1       | 2   | 1   | 0   | 0   | 5   |
| a2   | **_1_** | 1   | 0   | -1  | 1   | 3   |
| Z    | -1      | -1  | 0   | 1   | 0   | 0   |

The smallest negative values in the $Z$ row are the two -1s, so the first one, the $x_1$ column is selected as the pivot column. The ratios are calculated as follows:

- Base $s_1$ row: $5/1 = 5$
- Base $a_2$ row: $3/1 = 3$

The smallest positive ratio is 3, so the $a_2$ row is selected as the pivot row. The pivot element is already 1, so no row division needs to be performed.

The pivot row is subtracted from the first row, and added to the $Z$ row, making all other values in the pivot column 0:

| Base | x1  | x2  | s1  | s2  | a2  | RHS |
| ---- | --- | --- | --- | --- | --- | --- |
| s1   | 0   | 1   | 1   | 1   | -1  | 2   |
| x1   | 1   | 1   | 0   | -1  | 1   | 3   |
| Z    | 0   | 0   | 0   | 0   | 1   | 3   |

Phase 1 ends when none of the artificial variables are basis variables, which is the case here. The tableau now needs to prepare for phase 2.

#### Post Phase 1 Preparation

The artificial variables are removed from the tableau, and the objective function is reset to the original maximization problem. Remember from the No Artificial Variables section of Tableau setup that the objective function coefficients are negative:

| Base | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- |
| s1   | 0   | 1   | 1   | 1   | 2   |
|      | 1   | 1   | 0   | -1  | 3   |
| Z    | -2  | -1  | 0   | 0   | 0   |

Note that adding the objective function has made $x_1$ no longer a basis. This is solved by pivoting on the 1 element of the $x_1$ column:

| Base | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- |
| s1   | 0   | 1   | 1   | 1   | 2   |
| x1   | 1   | 1   | 0   | -1  | 3   |
| Z    | 0   | 1   | 0   | -2  | 6   |

The tableau is now ready for phase 2.

#### Phase 2

Phase 2 repeats the same pivoting process as phase 1, but with the objective function coefficients. This is repeaded until all values in the $Z$ row are non-negative.

For our example:

| Base | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- |
| s1   | 0   | 1   | 1   | 1   | 2   |
| x1   | 1   | 1   | 0   | -1  | 3   |
| Z    | 0   | 1   | 0   | -2  | 6   |

The pivot column is the $s_2$ column, and the $s_1$ basis row is the only row with a positive ratio. Pivoting on the 1 element of the $s_2$ column:

| Base | x1  | x2  | s1  | s2  | RHS |
| ---- | --- | --- | --- | --- | --- |
| s2   | 0   | 1   | 1   | 1   | 2   |
| x1   | 1   | 2   | 0   | 0   | 5   |
| Z    | 0   | 3   | 2   | 0   | 10  |

All of the elements of the $Z$ are non-negative, completing phase 2.

#### Results

Two extract final variable values from the tableau, we look at the base variable column. The variables in the column are equal to the corresponding RHS value. For our example:

$$ s_2 = 2 $$
$$ x_1 = 5 $$

All other variables are zero.

Our final objective value is the bottom right most value, in this example, $`Z = 10`$.

Thus, we get our final result for our optimization problem:

$$ x_1 = 5, x_2 = 0, Z = 10 $$

## Example Application

### Definitions

- $o =$ OFACer index, each person in the performance
- $r =$ row index, each performance
- $c =$ column index, each safety position
- $P =$ performer binary, where $P_{or}$ is $1$ when OFACer $o$ is performing in performance $r$
- $S =$ safety binary, where $S_{orc}$ is $1$ when OFACer $o$ is safetying in performance $r$ in safety position $c$
- $M =$ music master binary, where $M_{or}$ is $1$ when OFACer $o$ is the music master for performance $r$
- $E =$ experienced binary, where $E_{o}$ is $1$ if OFACer $o$ is allowed to be safety 1 or 4

### Givens

- Performance order
- Music masters

### Constraints

Only one role per person per row

$$P_{or} + \sum_{c=1}^{5}s_{orc} + m_{or} \le 1, \forall \ r \in R, \forall \ o \in O$$

Can't safety right before or after your performance

$$P_{or} \left( \sum_{c=1}^{5} \left( S_{o(r-1)c} + S_{o(r+1)c} \right) \right) = 0, \forall \ r \in R, \forall \ o \in O$$

Experienced safeties in slots 1 and 4

$$S_{or1} \le E_{o}, \forall \ r \in R, \forall \ o \in O$$

$$S_{or4} \le E_{o}, \forall \ r \in R, \forall \ o \in O$$

At least two safeties must stay the same between performances

$$\sum_{o=1}^{O} \sum_{c=1}^{C} S_{orc} * S_{o(r+1)c} \ge 2, \forall \ r \in R$$

### Optimization

$$\text{min } Z=\sum_{o=1}^{O} \left(\sum_{r=1}^{R} \sum_{c=1}^{C} s_{orc} - \frac{5|R|}{|O|}\right)^2$$

### Current limitations and possible improvements

- Performance order isn't optimized, and there may be infeasible performance orders
- Props aren't considered, so safety 5 is still filled for long props
- Optimize for minimizing swaps
- Include music master in optimization

## Setup

For this project, we used [numpy](https://numpy.org/) when implementing our Linear and Integer programming solvers. We also tested our constraints using [PuLP](https://coin-or.github.io/pulp/).

These packages are listed in [`requirements.txt`](./requirements.txt) and can be installed using `pip install -r requirements.txt`

## Resources

Listed here are the resources we used for this project:

- [The Two-phase Simplex Method: An Example](https://www.youtube.com/watch?v=_wnqe5_CLU0) - Sergiy Butenko
- [Simplex algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm) - Wikipedia
- [Branch and cut](https://en.wikipedia.org/wiki/Branch_and_cut) - Wikipedia
- [Cutting-plane method](https://en.wikipedia.org/wiki/Cutting-plane_method) - Wikipedia
- [Gomory Cuts and a little more](https://ocw.mit.edu/courses/15-053-optimization-methods-in-management-science-spring-2013/4717f89c50e91aaa455dbe9cb5a3e225_MIT15_053S13_tut11.pdf) - MIT OpenCourseWare
