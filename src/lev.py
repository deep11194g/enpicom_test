import numpy as np


def get_levenshtein_score(sequence1, sequence2):
    """
    Align two sequences and find the levenshtein score b/w them
    Addition, Deletion and Substitution are all valued as 1

    :param(str) sequence1: First Sequence
    :param(str) sequence2: Second Sequence
    :return(int): Levenshtein Score
    """
    num_rows = len(sequence1) + 1  # Parallel to column
    num_cols = len(sequence2) + 1  # Parallel to row

    distance_matrix = np.zeros((num_rows, num_cols))
    distance_matrix[0] = list(range(num_cols))  # 1st row
    distance_matrix[:, 0] = list(range(num_rows))  # 1st column

    for i in range(1, num_rows):
        for j in range(1, num_cols):
            substitutions = 0 if sequence1[i - 1] == sequence2[j - 1] else 1
            distance_matrix[i, j] = min(distance_matrix[i - 1, j] + 1, distance_matrix[i, j - 1] + 1,
                                        distance_matrix[i - 1, j - 1] + substitutions)

    return distance_matrix[num_rows - 1][num_cols - 1]
