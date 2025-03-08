from enum import Enum
from typing import Dict


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

    ARTIFICIAL_VAR_TAG = "ARTIFICIAL"
    SLACK_VAR_TAG = "SLACK"

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
                self.coef_map[f"{self.SLACK_VAR_TAG}_{constraint_idx}"] = 1
            case ConstraintType.GREATER_THAN:
                # Subtract slack variable and add artificial variable
                self.coef_map[f"{self.SLACK_VAR_TAG}_{constraint_idx}"] = -1
                self.coef_map[f"{self.ARTIFICIAL_VAR_TAG}_{constraint_idx}"] = 1
            case ConstraintType.EQUAL:
                # Add artificial variable
                self.coef_map[f"{self.ARTIFICIAL_VAR_TAG}_{constraint_idx}"] = 1
        self.ctype = ConstraintType.EQUAL
