def sort(array):
    shuffle(array)
    quick_sort_recursive(array, 0, len(array) - 1)

def shuffle(array):
    n = len(array)
    for i in range(0, n - 2):
        random_item_index = random.randint(i, n - 1)
        swap(array, i, random_item_index)

def quick_sort_recursive(array, left, right):
    # ...
    
def get_pivot(array, left, right):
    # The array is already shuffled, so the leftmost item will be random.
    return array[left]
