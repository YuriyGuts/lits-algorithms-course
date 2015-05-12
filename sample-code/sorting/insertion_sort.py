from sorting_algorithm import SortingAlgorithm


class InsertionSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        for i in range(1, len(array)):
            current_pos = i
            while current_pos > 0 and self.compare(array[current_pos], array[current_pos - 1]):
                self.swap(array, current_pos, current_pos - 1)
                current_pos -= 1
