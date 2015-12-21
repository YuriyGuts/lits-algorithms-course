def main():
    weights = read_input("weights01.txt")
    max_weight_sum, solutions = solve(weights)
    items_to_include = reconstruct_solution(solutions)
    write_output(weights, max_weight_sum, solutions, items_to_include)


def read_input(filename):
    with open(filename, "r") as input_file:
        weights = [int(weight)
                   for weight in input_file.read().split()]
    return weights


def solve(weights):
    # Remembering the solutions to smaller subproblems.
    solutions = [None for i in range(0, len(weights) + 1)]

    # Manually setting the solutions for the smallest possible subproblems.
    solutions[0] = 0
    solutions[1] = weights[0]

    for i in range(2, len(weights) + 1):
        # Either current vertex does not belong to an optimal solution...
        case1_solution = solutions[i - 1]
        # Or it does, then the previous one doesn't.
        case2_solution = solutions[i - 2] + weights[i - 1]

        # Which option is better?
        solutions[i] = max(case1_solution, case2_solution)

    # The answer to the largest subproblem is the answer to the original problem.
    return solutions[len(weights)], solutions


def reconstruct_solution(solutions):
    indices_to_include = []

    # Starting from the last element and stepping backwards, following the winning case every time.
    i = len(solutions) - 1
    while i >= 1:
        case_1_wins = solutions[i] == solutions[i - 1]
        if case_1_wins:
            # If case 1 won here, we'll just ignore this item.
            i -= 1
        else:
            # If case 2 won here, we'll remember this item and make 2 steps back.
            indices_to_include.insert(0, i - 1)
            i -= 2

    return indices_to_include


def write_output(weights, max_weight_sum, solutions, indices_to_include):
    print "--- Weights ---"
    print weights

    print "--- Subproblem Solutions ---"
    print solutions

    print "--- Indices to Include ---"
    print indices_to_include

    print "--- Max Sum ---"
    print max_weight_sum


if __name__ == "__main__":
    main()
