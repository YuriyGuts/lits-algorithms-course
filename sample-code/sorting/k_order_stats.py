import random


def main():
    array = generate_random_array(size=50, max_value=100)
    k = 5
    stat = find_k_order_statistic(array, k)

    print "Array:", array
    print "{0}-th order statistic: {1}".format(k, stat)
    print "Just to check - sorted array:", sorted(array)


def generate_random_array(size, max_value):
    return [random.randint(0, max_value) for _ in range(0, size)]


def find_k_order_statistic(array, k):
    array_copy = list(array)
    random.shuffle(array_copy)
    return find_k_order_statistic_recursive(array_copy, k, 0, len(array_copy) - 1)


def find_k_order_statistic_recursive(array, k, low, high):
    # The trick of the Randomized Selection algorithm is relying
    # on the QuickSort partitioning function to find the k-order statistic.
    #
    # If the partitioning function says that the pivot is now at position k,
    # then the pivot IS the statistic and we'll return it.
    # Otherwise, we'll look to the left or to the right from the pivot.
    if high < low:
        return array[low]

    pivot_pos = partition(array, low, high)
    if pivot_pos < k - 1:
        return find_k_order_statistic_recursive(array, k, pivot_pos + 1, high)
    else:
        return find_k_order_statistic_recursive(array, k, low, pivot_pos - 1)


def partition(array, low, high):
    # The partitioning function is the same as in QuickSort.
    left = min(low + 1, high)
    right = high

    pivot = array[low]

    while True:
        while array[left] <= pivot:
            if left == high:
                break
            left += 1

        while pivot <= array[right]:
            if right == low:
                break
            right -= 1

        if left >= right:
            break

        array[left], array[right] = array[right], array[left]

    array[low], array[right] = array[right], array[low]
    return right


if __name__ == "__main__":
    main()
