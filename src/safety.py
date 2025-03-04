import numpy as np
import io_handle

# define o as list of performers
# define r as rows of performances
# define c as number of safety pos


# Gather the indicies of each perfance and ofacer from the input
filepath = "mock_input.csv"
ofacers = io_handle.get_groups(filepath, False)
o = np.array([], dtype=int)
r = np.array([], dtype=int)
for i, group in enumerate(ofacers):
    r = np.append(r, i)
    for ofacer in group:
        o = np.append(o, int(ofacer))
print(f"{o=}")
print(f"{r=}")

# Define collumns
C = 5  # can change this value to modify the amount of safety slots
c = np.array([], int)
for i in range(C):
    c = np.append(c, i)
print(f"{c=}")
