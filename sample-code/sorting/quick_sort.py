from sorting_algorithm import SortingAlgorithm
import random


class QuickSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        random.shuffle(array)
        self.quicksort_recursive(array, 0, len(array) - 1)

    def quicksort_recursive(self, array, low, high):
        if high <= low:
            return

        pivot_pos = self.partition(array, low, high)
        self.quicksort_recursive(array, low, pivot_pos - 1)
        self.quicksort_recursive(array, pivot_pos + 1, high)

    def partition(self, array, low, high):
        left = low + 1
        right = high

        pivot = array[low]

        while True:
            while not self.compare(pivot, array[left]):
                if left == high:
                    break
                left += 1

            while not self.compare(array[right], pivot):
                if right == low:
                    break
                right -= 1

            if left >= right:
                break

            self.swap(array, left, right)

        self.swap(array, low, right)
        return right
