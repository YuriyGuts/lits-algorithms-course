def sort(array):
    result = merge_sort_recursive(array, 0, len(array) - 1)

    # Replacing the input array with the sorted result.
    for i in range(0, len(result)):
        array[i] = result[i]


def merge_sort_recursive(array, left, right):
    if left < right:
        middle = (left + right) / 2

        # Splitting the larger task into smaller subtasks and solving each recursively.
        left_part = merge_sort_recursive(array, left, middle)
        right_part = merge_sort_recursive(array, middle + 1, right)

        # Merging the results of the subproblems.
        result = merge(left_part, right_part)

        return result

    # If our [left..right] range contains only one item, returning it.
    return [array[left]]


def merge(left_array, right_array):
    # Creating an auxiliary array for storing the merged result.
    result = [None] * (len(left_array) + len(right_array))

    # Remembering the reading positions for both subarrays.
    left_pos = right_pos = result_pos = 0

    # Picking items either from the left subarray or the right subarray,
    # depending on which item is smaller.
    while result_pos < len(result):
        # If we have no more items on the left OR right item is smaller than left
        # then pick from the right subarray.
        if left_pos >= len(left_array) or (right_pos < len(right_array) and 
                compare(right_array[right_pos], left_array[left_pos])):
            result[result_pos] = right_array[right_pos]
            right_pos += 1
        # ...otherwise, pick from the left one.
        else:
            result[result_pos] = left_array[left_pos]
            left_pos += 1

        result_pos += 1

    return result
