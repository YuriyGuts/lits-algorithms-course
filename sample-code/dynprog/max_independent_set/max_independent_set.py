def main():
    weights = read_input("weights01.txt")
    max_weight_sum = solve(weights)
    write_output(None, max_weight_sum)


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
    return solutions[len(weights)]


def write_output(filename, solution):
    if filename is None:
        print solution
        return

    with open(filename, "w") as output_file:
        output_file.write(solution)


if __name__ == "__main__":
    main()
