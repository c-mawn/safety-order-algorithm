from pulp import *
import numpy as np
from pulp.pulp import LpVariable

# Create the LP problem object
prob = LpProblem("Safety-Order-Optimization", LpMinimize)

# Define a binary type for easier type hinting
binary = Literal[0] | Literal[1]

# Define performers 
performer_names: list[str] = [
    'Avery',
    'Sarah',
    'Becca',

    'Lucien',

    'Kate',
    'Trinity',

    'Noah',
    'Maddie',
    'Leo',

    'Ben',
    'Jacob',

    'KD',
    'Aditi',

    'Dominic',
    'Beck',

    'Aja',

    'Hugh',
    'Kelly',
]

# Define the performers matrix, which is given as an input
''' P: list[list[binary]] = [
    [1,1,1,  0,  0,0,  0,0,0,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  1,  0,0,  0,0,0,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  1,1,  0,0,0,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  1,1,1,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  1,1,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,1,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  0,0,  1,1,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  0,0,  0,0,  1,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  0,0,  0,0,  0,  1,1,],
] '''

P: np.ndarray[Any, np.dtype[np.bool]] = np.array([
    [1,1,1,  0,  0,0,  0,0,0,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  1,  0,0,  0,0,0,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  1,1,  0,0,0,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  1,1,1,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  1,1,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,1,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  0,0,  1,1,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  0,0,  0,0,  1,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  0,0,  0,0,  0,  1,1,],
])

# Define the music master matrix, which is given as an input
''' M: list[list[binary]] = [
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,1,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,1,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,1,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,1,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,1,  0,0,  0,0,  0,  0,0,],
] '''

M: np.ndarray[Any, np.dtype[np.bool]] = np.array([
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,0,  1,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,1,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,1,  0,0,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,1,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,1,  0,0,  0,0,  0,  0,0,],
    [0,0,0,  0,  0,0,  0,0,0,  0,1,  0,0,  0,0,  0,  0,0,],
])

# Define the experienced list, which is a whitelist for safety slots 1 and 4
''' E: list[binary] = [
    0,0,0,  1,  1,0,  0,0,0,  1,1,  1,1,  1,1,  1,  1,1,
] '''

E: np.ndarray[Any, np.dtype[np.bool]] = np.array([
    0,0,0,  1,  1,0,  0,0,0,  1,1,  1,1,  1,1,  1,  1,1,
])

# Validate that the performers matrix and music master matrix are correct
# print(f'|{'PERFORMERS':<30}|{'MUSIC MASTERS':<30}|')
# for r, performance in enumerate(P):
#     print(f'|{', '.join([name for i, name in enumerate(performer_names) if performance[i]]):<30}|{', '.join([name for i, name in enumerate(performer_names) if M[r][i]]):<30}|')
# 
# print()
# 
# Validate that the experienced list is correct
# print('EXPERIENCED SAFETIES:')
# print('\n'.join([f'- {name}' for i, name in enumerate(performer_names) if E[i]]))

# Define index maxes
O = len(performer_names)
R = len(P)

# Define the safety matrix
S = [[[
    LpVariable(f'S_{o}_{r}_{c}', cat=LpBinary)
    for c in range(5)]
    for r in range(R)]
    for o in range(O)]

Delta = LpVariable('Delta', lowBound=0)

# Add optimization function
mean_safties = 5*R/O
prob += Delta
for o in range(O):
    prob += Delta >= (mean_safties - sum([sum([S[o][r][c] for c in range(5)]) for r in range(R)]))
    prob += (mean_safties - sum([sum([S[o][r][c] for c in range(5)]) for r in range(R)])) >= -Delta

# All safety slots need to have exactly 1 person 
for c in range(5):
    for r in range(R):
        prob += sum([S[o][r][c] for o in range(O)]) == 1

# Only one role per person per row
for o in range(O):
    for r in range(R):
        prob += P[r][o] + sum([S[o][r][c] for c in range(5)]) + M[r][o] <= 1

# Can't safety right before or after your performance
for o in range(O):
    for r in range(1, R-1):
        prob += P[r][o] * sum([S[o][r-1][c] + S[o][r+1][c] for c in range(5)]) == 0

    prob += P[0][o] * sum([S[o][1][c] for c in range(5)]) == 0
    prob += P[R-1][o] * sum([S[o][R-2][c] for c in range(5)]) == 0

# Experienced safeties in slots 1 and 4
for o in range(O):
    for r in range(R):
        prob += S[o][r][0] <= E[o]
        prob += S[o][r][3] <= E[o]

# No more than two swaps
# Create another variable to keep track of swaps (S_orc * S_o(r+1)c)
W: list[list[list[LpVariable]]] = [[[
    LpVariable(f'W_{o}_{r}_{c}', cat=LpBinary)
    for c in range(5)]
    for r in range(R-1)]
    for o in range(O)]

# Constrain W_orc to be S_orc * S_o(r+1)c
for o in range(O):
    for r in range(R-1): 
        for c in range(5): 
            prob += W[o][r][c] <= S[o][r][c]
            prob += W[o][r][c] <= S[o][r+1][c]
            prob += W[o][r][c] >= S[o][r][c] + S[o][r+1][c] - 1

# Constrain swaps
for r in range(R-1): 
    prob += sum([sum([W[o][r][c] for c in range(5)]) for o in range(O)]) >= 3

# Solve problem
prob.solve()

# Print results:
print (("Status:"), LpStatus[prob.status])

for r in range(R):
    for c in range(5):
        for o in range(O):
            if S[o][r][c].value() == 1:
                print(f'{performer_names[o]:<10}', end='')
    print()