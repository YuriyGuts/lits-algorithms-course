def main():
    string1, string2, penalties = read_input("sequence01.txt")
    min_penalty, alignment1, alignment2 = solve(string1, string2, penalties)
    write_output(None, min_penalty, alignment1, alignment2)


def read_input(filename):
    with open(filename, "r") as input_file:
        string1 = input_file.readline().strip()
        string2 = input_file.readline().strip()

        # Assuming only two types of penalties for this problem:
        # the one for matching different letters, and the one for matching a letter with a gap.
        penalties = [int(penalty) for penalty in input_file.readline().split()]
        penalties = {
            "different_letters": penalties[0],
            "gap": penalties[1],
        }

        # For convenience, let's make sure the 1st string cannot be shorter than the 2nd.
        if len(string1) < len(string2):
            string1, string2 = string2, string1

        return string1, string2, penalties


def solve(string1, string2, penalties):
    INFINITY = 10 ** 9

    # The solutions array uses 1-based indexing, while Python strings use 0-based.
    solutions = [[INFINITY for j in range(0, len(string1) + 1)] for i in range(0, len(string1) + 1)]

    # Initializing the solutions for the smallest subproblems.
    # Basically, [i][0] or [0][i] means that we haven't consumed any characters from one of the strings,
    # and inserted only spaces so far. Hence i * penalties["gap"] for each i.
    for i in range(0, len(string1) + 1):
        solutions[i][0] = solutions[0][i] = i * penalties["gap"]

    for i in range(1, len(string1) + 1):
        for j in range(1, len(string2) + 1):
            # Either we consume one letter from both strings...
            case1 = solutions[i - 1][j - 1] + (penalties["different_letters"] if string1[i - 1] != string2[j - 1] else 0)
            # ...or consume a letter from the 1st string and insert a gap into the 2nd...
            case2 = solutions[i - 1][j] + penalties["gap"]
            # ...or consume a letter from the 2nd string and insert a gap into the 1st.
            case3 = solutions[i][j - 1] + penalties["gap"]

            # Which one gives us a smaller overall penalty?
            solutions[i][j] = min(case1, case2, case3)

    # Optional step: if we are interested not only in the overall penalty, but in the actual alignments,
    # we'll run a reverse algorithm to reconstruct the aligned strings from the solution array.
    alignment1, alignment2 = reconstruct_alignments(string1, string2, solutions, penalties)

    # The solution to the initial problem would be the result of aligning the last two letters.
    min_overall_penalty = solutions[len(string1)][len(string2)]

    return min_overall_penalty, alignment1, alignment2


def reconstruct_alignments(string1, string2, solutions, penalties):
    alignment1 = ""
    alignment2 = ""

    # Running the algorithm backwards: starting from the end cell, checking which case brought us here.
    i = len(string1)
    j = len(string2)

    while not (i == 0 and j == 0):
        case1 = solutions[i - 1][j - 1] + (penalties["different_letters"] if string1[i - 1] != string2[j - 1] else 0)
        case2 = solutions[i - 1][j] + penalties["gap"]
        case3 = solutions[i][j - 1] + penalties["gap"]

        solution = min(case1, case2, case3)
        if solution == case1:
            # We must have decided to consume a letter from both strings.
            alignment1 = string1[i - 1] + alignment1
            alignment2 = string2[j - 1] + alignment2
            i -= 1
            j -= 1
        elif solution == case2:
            # We must have decided to consume a letter from the 1st string and insert a gap into the 2nd.
            alignment1 = string1[i - 1] + alignment1
            alignment2 = " " + alignment2
            i -= 1
        elif solution == case3:
            # We must have decided to consume a letter from the 2nd string and insert a gap into the 1st.
            alignment1 = " " + alignment1
            alignment2 = string2[j - 1] + alignment2
            j -= 1

    return alignment1, alignment2


def write_output(filename, min_penalty, alignment1, alignment2):
    if filename is None:
        print alignment1
        print alignment2
        print min_penalty
        return

    with open(filename, "w") as output_file:
        output_file.write("%s\n" % alignment1)
        output_file.write("%s\n" % alignment2)
        output_file.write("%d\n" % min_penalty)


if __name__ == "__main__":
    main()
