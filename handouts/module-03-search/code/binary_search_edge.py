def binary_search_leftmost(sorted_haystack, needle):
    # A modification of binary search that finds the leftmost element among equals.
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

    return None


def binary_search_rightmost(sorted_haystack, needle):
    # A modification of binary search that finds the rightmost element among equals.
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

    return None
