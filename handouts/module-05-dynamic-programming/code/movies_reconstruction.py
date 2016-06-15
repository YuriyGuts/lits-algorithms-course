def reconstruct_solution(solutions):
    indices_to_include = []

    # We start from the last element and step backwards,
    # following the winning case every time.
    i = len(solutions) - 1
    while i >= 1:
        case_1_wins = solutions[i] == solutions[i - 1]
        if case_1_wins:
            # If case 1 won here, we'll just ignore this item.
            i -= 1
        else:
            # If case 2 won here, we'll remember this item and take 2 steps back.
            indices_to_include.insert(0, i - 1)
            i -= 2

    return indices_to_include
