def sort(array):
    # Creating an auxiliary array for storing the merged result.
    merge_results = [0] * len(array)
    merge_sort_recursive(array, merge_results, 0, len(array) - 1)


def merge_sort_recursive(array, merge_results, left, right):
    if left < right:
        middle = (left + right) // 2
        
        # Splitting the larger task into smaller subtasks and solving each recursively.
        merge_sort_recursive(array, merge_results, left, middle)
        merge_sort_recursive(array, merge_results, middle + 1, right)

        # Merging the results of the subproblems.
        merge(array, merge_results, left, middle + 1, right)


def merge(array, merge_results, left_begin, right_begin, right_end):
    # Remembering the reading positions for both subarrays.
    left_end = right_begin - 1
    left_read_pos = left_begin
    right_read_pos = right_begin
    result_write_pos = left_begin

    # Picking items either from the left subarray or the right subarray,
    # depending on which item is smaller.
    while left_read_pos <= left_end and right_read_pos <= right_end:
        if compare(array[left_read_pos], array[right_read_pos]):
            merge_results[result_write_pos] = array[left_read_pos]
            left_read_pos += 1
        else:
            merge_results[result_write_pos] = array[right_read_pos]
            right_read_pos += 1
        result_write_pos += 1

    # If we have no more items on the right then pick from the left subarray.
    while left_read_pos <= left_end:
        merge_results[result_write_pos] = array[left_read_pos]
        left_read_pos += 1
        result_write_pos += 1

    # If we have no more items on the left then pick from the right subarray.
    while right_read_pos <= right_end:
        merge_results[result_write_pos] = array[right_read_pos]
        right_read_pos += 1
        result_write_pos += 1

    array[left_begin:right_end + 1] = merge_results[left_begin:right_end + 1]
