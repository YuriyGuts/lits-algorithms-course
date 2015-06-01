def sort(array):
    for i in range(1, len(array)):
        current_pos = i

        # If the left neighbor exists and it's larger than our current item,
        # swap them and check the next left neighbor.
        while current_pos > 0 and compare(array[current_pos], array[current_pos - 1]):
            swap(array, current_pos, current_pos - 1)
            current_pos -= 1
