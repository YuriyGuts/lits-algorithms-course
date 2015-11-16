import random


def main():
    array = generate_random_array(50)
    array = sorted(array)

    pos = binary_search(array, 5)
    print array
    print pos


def generate_random_array(size):
    return [random.randint(0, 100) for _ in range(0, size)]


def binary_search(sorted_haystack, needle):
    left = 0
    right = len(sorted_haystack) - 1

    while left <= right:
        middle = (left + right) // 2

        if sorted_haystack[middle] == needle:
            return middle

        if sorted_haystack[middle] > needle:
            right = middle - 1
        else:
            left = middle + 1

    return -1


if __name__ == "__main__":
    main()