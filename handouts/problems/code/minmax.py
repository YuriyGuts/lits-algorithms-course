import sys


def main():
    input_filename = "minmax.in" if len(sys.argv) == 1 else sys.argv[1]
    output_filename = "minmax.out" if len(sys.argv) == 1 else sys.argv[2]

    array = read_input(input_filename)
    minimum, maximum = solve(array)
    write_output(output_filename, minimum, maximum)


def read_input(filename):
    with open(filename, "r") as input_file:
        array_str = input_file.readline()
        array = [int(item) for item in array_str.split()]
        return array


def solve(array):
    minimum = min(array)
    maximum = max(array)
    return minimum, maximum


def write_output(filename, minimum, maximum):
    with open(filename, "w") as output_file:
        output_file.write("{minimum} {maximum}".format(**locals()))


if __name__ == "__main__":
    main()
