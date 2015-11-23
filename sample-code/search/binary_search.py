import random


def main():
    array = generate_random_array(size=50, max_value=20)
    array = sorted(array)

    value_to_find = 2
    print "Array:"
    print array
    print

    print "Finding the position of element '{0}':".format(value_to_find)
    print "Simple binary search:", binary_search(array, value_to_find)
    print "Leftmost binary search:", binary_search_leftmost(array, value_to_find)
    print "Rightmost binary search:", binary_search_rightmost(array, value_to_find)


def generate_random_array(size, max_value):
    return [random.randint(0, max_value) for _ in range(0, size)]


def binary_search(sorted_haystack, needle):
    # To avoid recursion, we'll use these variables to limit
    # the scope of the search, and use a while loop instead.
    left = 0
    right = len(sorted_haystack) - 1

    while left <= right:
        # Looking at the middle element.
        middle = (left + right) // 2

        # If we're lucky and have found the element we're looking for, returning its position.
        if sorted_haystack[middle] == needle:
            return middle

        # If the middle element is greater than the value we're searching,
        # we're not interested in the right part anymore.
        if sorted_haystack[middle] > needle:
            right = middle - 1
        # If the middle element is smaller, we're not interested in the left part.
        else:
            left = middle + 1

    return -1


def binary_search_leftmost(sorted_haystack, needle):
    # A modification of the binary search algorithm that finds the leftmost element among equals.
    # E.g., for [0, 1, 1, 2, 2, 2, 3, 3] the element '2' will be found at position 3.
    left = 0
    right = len(sorted_haystack) - 1

    while right - left > 1:
        middle = left + (right - left) / 2
        if sorted_haystack[middle] >= needle:
            right = middle
        else:
            left = middle

    if sorted_haystack[right] == needle:
        return right

    return -1


def binary_search_rightmost(sorted_haystack, needle):
    # A modification of the binary search algorithm that finds the rightmost element among equals.
    # E.g., for [0, 1, 1, 2, 2, 2, 3, 3] the element '2' will be found at position 5.
    left = 0
    right = len(sorted_haystack) - 1

    while right - left > 1:
        middle = left + (right - left) / 2
        if sorted_haystack[middle] <= needle:
            left = middle
        else:
            right = middle

    if sorted_haystack[left] == needle:
        return left

    return -1


if __name__ == "__main__":
    main()
