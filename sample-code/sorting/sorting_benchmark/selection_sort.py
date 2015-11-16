from sorting_algorithm import SortingAlgorithm


class SelectionSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        for i in range(0, len(array)):
            min_index = i
            for j in range(i + 1, len(array)):
                if self.compare(array[j], array[min_index]):
                    min_index = j
            self.swap(array, i, min_index)
