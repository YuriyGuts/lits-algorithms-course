class SortingAlgorithm:
    def __init__(self, compare_function):
        self.compare = compare_function

    def sort(self, array):
        pass

    def swap(self, array, index1, index2):
        (array[index1], array[index2]) = (array[index2], array[index1])
