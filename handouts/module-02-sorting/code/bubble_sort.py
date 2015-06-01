def sort(array):
    is_sorted = False

    # Repeat until there are no changes made to the array.
    while not is_sorted:
        is_sorted = True

        # Scanning through neighbors and swapping them if necessary.
        for i in range(1, len(array)):
            if compare(array[j], array[j - 1]):
                swap(array, j, j - 1)
                is_sorted = False
