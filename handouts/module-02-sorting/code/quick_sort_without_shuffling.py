def sort(array):
    quick_sort_recursive(array, 0, len(array) - 1)

def quick_sort_recursive(array, left, right):
    pivot = get_pivot(array, left, right)
    left_write_pos = left
    right_write_pos = right

    # Moving two pointers through the array: one from the left
    # and one from the right. Every time the left item is greater
    # than the pivot and the right item is less, we swap them.
    while left_write_pos <= right_write_pos:

        while compare(array[left_write_pos], pivot):
            left_write_pos += 1

        while compare(pivot, array[right_write_pos]):
            right_write_pos -= 1

        if left_write_pos <= right_write_pos:
            swap(array, left_write_pos, right_write_pos)
            left_write_pos += 1
            right_write_pos -= 1

    # Sort left and right part recursively, if they are not empty.
    if left < left_write_pos - 1:
        quick_sort_recursive(array, left, left_write_pos - 1)

    if left_write_pos < right:
        quick_sort_recursive(array, left_write_pos, right)

def get_pivot(array, left, right):
    # Take the leftmost item by default.
    return array[left]
