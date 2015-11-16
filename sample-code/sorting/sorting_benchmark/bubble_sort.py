from sorting_algorithm import SortingAlgorithm


class BubbleSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        for i in range(0, len(array)):
            for j in range(1, len(array) - i):
                if self.compare(array[j], array[j - 1]):
                    self.swap(array, j, j - 1)
