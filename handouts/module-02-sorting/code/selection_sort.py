def sort(array):
    N = len(array)

    for i in range(0, N - 1):
        min_index = i

        # Looking for the minimum among [i+1 .. N-1]
        for j in range(i + 1, N):
            if compare(array[j], array[min_index]):
                min_index = j

        # Swapping the elements on positions 'i' and 'min_index'.
        swap(array, i, min_index)
