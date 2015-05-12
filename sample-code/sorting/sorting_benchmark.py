import random
import timeit


class SortingBenchmark:

    def __init__(self, input_size=20):
        self.__comparisons = 0
        self.__exchanges = 0
        self.__input_size = input_size

    def run(self, algorithm, input=None):
        self.__comparisons = 0
        self.__exchanges = 0

        # Replacing the original 'swap' and 'compare' functions with decorators
        # so that we're able to track the number of exchanges/comparisons.
        original_swap_function = algorithm.swap
        original_compare_function = algorithm.compare

        def countable_swap(array, index1, index2):
            self.__exchanges += 1
            original_swap_function(array, index1, index2)

        def countable_compare(a, b):
            self.__comparisons += 1
            return original_compare_function(a, b)

        algorithm.swap = countable_swap
        algorithm.compare = countable_compare

        # Generating a random array if no input is provided.
        if input is None:
            input = self.generate_random_array()

        # Measuring algorithm execution time.
        timer = timeit.Timer(lambda: algorithm.sort(input))
        seconds_elapsed = timer.timeit(1)

        # Restoring the old 'swap' and 'compare' functions.
        algorithm.swap = original_swap_function
        algorithm.compare = original_compare_function

        return seconds_elapsed, self.__comparisons, self.__exchanges

    def generate_random_array(self):
        return list([random.randint(0, 100) for _ in range(0, self.__input_size)])
