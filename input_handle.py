"""
File to handle the input for the safety order algorithm
"""

import csv


def get_groups(filepath, keep_empty_slots=False):
    """
    Given a csv containing the groups for a performance, outputs the groups
    in the form of a list containing lists of the performers in each group.

    Args:
        filepath: string representing the filepath of the csv file

        keep_empty_slots: default False: boolean representing whether the
            output list contains empty string representative of the empty
            performer slots.

    Returns:
        groups: list of lists containing each performer group, in no particular
            order.
    """
    groups = []
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not keep_empty_slots:
                while "" in row:
                    row.remove("")
            groups.append(row)
    return groups
