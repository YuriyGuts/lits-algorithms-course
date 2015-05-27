from sorting_algorithm import SortingAlgorithm
import random


class QuickSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        self.shuffle(array)
        self.quick_sort_recursive(array, 0, len(array) - 1)

    def shuffle(self, array):
        n = len(array)
        for i in range(0, n - 2):
            random_item_index = random.randint(i, n - 1)
            self.swap(array, i, random_item_index)

    def quick_sort_recursive(self, array, left, right):
        pivot = self.get_pivot(array, left, right)
        left_write_pos = left
        right_write_pos = right

        while left_write_pos <= right_write_pos:

            while self.compare(array[left_write_pos], pivot):
                left_write_pos += 1

            while self.compare(pivot, array[right_write_pos]):
                right_write_pos -= 1

            if left_write_pos <= right_write_pos:
                self.swap(array, left_write_pos, right_write_pos)
                left_write_pos += 1
                right_write_pos -= 1

        if left < left_write_pos - 1:
            self.quick_sort_recursive(array, left, left_write_pos - 1)

        if left_write_pos < right:
            self.quick_sort_recursive(array, left_write_pos, right)

    def get_pivot(self, array, left, right):
        # Assuming the array is already shuffled
        return array[left]
