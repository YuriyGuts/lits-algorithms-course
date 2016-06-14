# Manually setting the solutions for the smallest possible subproblems.
solutions[0] = 0
solutions[1] = ratings[0]

for i in range(2, len(ratings) + 1):
    # Either current movie does not belong to an optimal solution...
    case1_solution = solutions[i - 1]
    # Or it does, then the previous one doesn't.
    case2_solution = solutions[i - 2] + ratings[i - 1]

    # Which option is better?
    solutions[i] = max(case1_solution, case2_solution)

# The answer to the largest subproblem is the answer to the original problem.
return solutions[len(ratings)]
