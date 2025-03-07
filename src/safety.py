import numpy as np
import io_handle
import two_phase_simplex

# define o as list of performers
# define r as rows of performances
# define c as number of safety pos


# Gather the indicies of each perfance and ofacer from the input
filepath = "mock_input.csv"
ofacers = io_handle.get_groups(filepath, False)
print(ofacers)

o = np.array([], dtype=int)
o_str = np.array([], dtype=str)
r = np.array([], dtype=int)
m = np.array([], dtype=str)
k = 0
for i, group in enumerate(ofacers):
    r = np.append(r, i)
    for ofacer in group[:-1]:
        o = np.append(o, k)
        o_str = np.append(o_str, ofacer)
        k += 1
    m = np.append(m, group[-1])
print(f"{o=}")
print(f"{o_str=}")
print(f"{r=}")
print(f"{m=}")

# Define collumns
C = 5  # can change this value to modify the amount of safety slots
c = np.array([], int)
for i in range(C):
    c = np.append(c, i)
print(f"{c=}")

# define P_or: Perfomer bool whether ofacer o is performing in row r

performer_dict = {}
for row, group in enumerate(ofacers):
    for ofacer_num, ofacer_name in enumerate(o_str):
        if ofacer_name in group:
            performer_dict.update({(ofacer_num, row): 1})
        else:
            performer_dict.update({(ofacer_num, row): 0})
print(f"{performer_dict=}")

# define m_or: dict of keys of each ofacer : whether they are the music master at row r
mus_mast_dict = {}
for row in r:
    for ofacer_num, ofacer_name in enumerate(o_str):
        if ofacer_name is m[r]:
            mus_mast_dict.update({(ofacer_num, row): 1})
        else:
            mus_mast_dict.update({(ofacer_num, row): 0})


# Sum from ofacer 0 to O of each Safety must be 1 for all rows in R, for all column in [1,5]

constraint_list_1 = []
for row in r:
    for col in c:
        con_dict = {}
        for ofacer in o:
            con_dict.update({f"S_{row}-{col}-{ofacer}": 1})
        con = two_phase_simplex.LPConstraint(
            con_dict, two_phase_simplex.ConstraintType.EQUAL, 1
        )
        constraint_list_1.append(con)
print(constraint_list_1)

# Only one role per person per row
# Performer_or + sum of each col of safety_orc + mus_master leq 1 for row in R for ofacer in O

constraint_list_2 = []
for row in r:
    for ofacer in o:
        p_or = performer_dict[(ofacer, row)]
        m_or = mus_mast_dict[(ofacer, row)]
        con_dict = {}
        for col in c:
            con_dict.update({f"S_{row}-{ofacer}-{col}": 1})
        con_dict.update({f"P_{row}-{ofacer}": p_or})
        con_dict.update({f"m_{row}-{ofacer}": m_or})
        con = two_phase_simplex.LPConstraint(
            con_dict, two_phase_simplex.ConstraintType.LESS_THAN, 1
        )
        constraint_list_2.append(con)
print(constraint_list_2)


# Cant safety right before or after your performace
# P_or * (sum of safeties_o(r-1)c + S_o(r+1)c for each col) = 0 for all rows and ofacers

constraint_list_3 = []
for row in r:
    for ofacer in o:
        p_or = performer_dict[(ofacer, row)]
        con_dict = {}
        for col in c:
            if p_or:
                if row is 0:
                    con_dict.update({f"S_{ofacer}-{row+1}-{col}": 1})
                elif row is r[-1]:
                    con_dict.update({f"S_{ofacer}-{row-1}-{col}": 1})
                else:
                    con_dict.update(
                        {f"S_{ofacer}-{row-1}-{col}": 1, f"S_{ofacer}-{row+1}-{col}": 1}
                    )
                con = two_phase_simplex.LPConstraint(
                    con_dict, two_phase_simplex.ConstraintType.EQUAL, 0
                )
                constraint_list_3.append(con)
print(constraint_list_3)
