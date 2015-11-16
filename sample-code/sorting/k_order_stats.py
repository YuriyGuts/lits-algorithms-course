import random


def main():
    array = generate_random_array(50)
    print array
    stat = find_k_order_statistic(array, 10)
    print array[stat]


def generate_random_array(size):
    return [random.randint(0, 100) for _ in range(0, size)]


def find_k_order_statistic(array, k):
    random.shuffle(array)
    return find_k_order_statistic_recursive(array, k, 0, len(array) - 1)


def find_k_order_statistic_recursive(array, k, low, high):
    if high <= low:
        return low

    pivot_pos = partition(array, low, high)
    if pivot_pos < k - 1:
        return find_k_order_statistic_recursive(array, k, pivot_pos + 1, high)
    else:
        return find_k_order_statistic_recursive(array, k, low, pivot_pos - 1)


def partition(array, low, high):
    left = low + 1
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