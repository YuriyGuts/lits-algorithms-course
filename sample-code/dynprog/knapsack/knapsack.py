def main():
    capacity, items = read_input("knapsack01.txt")
    max_value = solve(capacity, items)
    write_output(None, max_value)


def read_input(filename):
    with open(filename, "r") as input_file:
        capacity = int(input_file.readline())
        items = [KnapsackItem(value=int(item_parameters[0]), weight=int(item_parameters[1]))
                 for item_parameters in [item_line.split() for item_line in input_file.readlines()]]
    return capacity, items


def solve(capacity, items):
    solutions = [[None for weight in range(0, capacity + 1)] for item_index in range(0, len(items) + 1)]

    # Initializing the solutions for the smallest subproblems.
    # If we have 0 items, we can have a maximum total item value of 0 for any knapsack capacity.
    for weight in range(0, capacity + 1):
        solutions[0][weight] = 0

    for index, item in enumerate(items):
        # Our items use 1-based indexing, so we'll increment the index to avoid confusion.
        index += 1

        for weight in range(0, capacity + 1):
            # Either we don't take the current item at all...
            case1_solution = solutions[index - 1][weight]

            # ...or we do, then the previous items will be an optimal solution for a smaller knapsack.
            if weight >= item.weight:
                case2_solution = solutions[index - 1][weight - item.weight] + item.value
            else:
                case2_solution = -1

            # Which case is better?
            solutions[index][weight] = max(case1_solution, case2_solution)

    return solutions[len(items)][capacity]


def write_output(filename, max_weight):
    if filename is None:
        print max_weight
        return

    with open(filename, "w") as output_file:
        output_file.write(max_weight)


class KnapsackItem:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __str__(self):
        return "Value: %d   Weight:%d" % (self.value, self.weight)


if __name__ == "__main__":
    main()
