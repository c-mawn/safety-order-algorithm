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
        groups: list of lists containing each performer group, where each
            list's final element is the music master for the performance

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


def make_safety_csv(safeties, filepath="output.csv"):
    """
    Given a list of lists containing all the safeties in order,
    outputs a csv file containing that information

    Args:
        Safeties: list of lists containing the safeties in their slots
        filepath: default to "output.csv", names the file that is created
            by the output of the function
    """
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerows(safeties)
