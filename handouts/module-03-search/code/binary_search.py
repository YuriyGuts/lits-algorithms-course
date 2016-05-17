def binary_search(sorted_haystack, needle):
    # To avoid recursion, we'll use these variables to limit
    # the scope of the search, and use a while loop instead.
    left = 0
    right = len(sorted_haystack) - 1

    while left <= right:
        # Looking at the middle element.
        middle = (left + right) // 2

        # If we're lucky and have found the element we're looking for,
        # returning its position.
        if sorted_haystack[middle] == needle:
            return middle

        # If the middle element is greater than the value we're searching,
        # we're not interested in the right part anymore.
        if sorted_haystack[middle] > needle:
            right = middle - 1
        # If it's smaller, we're not interested in the left part.
        else:
            left = middle + 1

    # We haven't found anything.
    return None
