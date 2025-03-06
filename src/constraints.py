from enum import Enum
from typing import Dict
import numpy as np
from numpy.typing import NDArray


class Role(Enum):
    PERFORMER = 0
    SAFETY_1 = 1
    SAFETY_2 = 2
    SAFETY_3 = 3
    SAFETY_4 = 4
    SAFETY_5 = 5
    MUSIC = 6

    def safeties():
        return [
            Role.SAFETY_1,
            Role.SAFETY_2,
            Role.SAFETY_3,
            Role.SAFETY_4,
            Role.SAFETY_5,
        ]


class LPVariable:
    def __init__(self, role: Role, ofacer: int, row: int):
        self.role = role
        self.ofacer = ofacer
        self.row = row

    def __eq__(self, other):
        return (
            self.role == other.role
            and self.ofacer == other.ofacer
            and self.row == other.row
        )

    def __hash__(self):
        return hash((self.role, self.ofacer, self.row))

    def __repr__(self):
        return f"{self.role.name}_{self.ofacer}_{self.row}"


def init_column_map() -> Dict[LPVariable, int]:
    column_map: Dict[LPVariable, int] = {}
    for o in range(num_ofacer):
        for row in range(performances):
            for role in Role:
                column_map[LPVariable(role, o, row)] = len(column_map)
    return column_map


def one_role_per_person_per_row(column_map: Dict[LPVariable, int]) -> NDArray:
    A: NDArray
    # only one role per person per row
    for o in range(num_ofacer):
        for row in range(performances):
            constraint_row = np.zeros(len(column_map))
            for role in Role:
                constraint_row[column_map[LPVariable(role, o, row)]] = 1


num_ofacer = 1
performances = 2
column_map = init_column_map()
print(column_map)
one_role_per_person_per_row(column_map)

# A: NDArray = np.empty((2))
# q = np.vstack((A, np.zeros(2)))
# print(q)
