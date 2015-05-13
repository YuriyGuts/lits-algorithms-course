from sorting_algorithm import SortingAlgorithm


class MergeSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        result = self.merge_sort_recursive(array, 0, len(array) - 1)
        for i in range(0, len(result)):
            array[i] = result[i]

    def merge_sort_recursive(self, array, left, right):
        if left < right:
            middle = (left + right) / 2
            left_part = self.merge_sort_recursive(array, left, middle)
            right_part = self.merge_sort_recursive(array, middle + 1, right)
            result = self.merge(left_part, right_part)
            return result

        return [array[left]]

    def merge(self, left_array, right_array):
        result = [None] * (len(left_array) + len(right_array))
        left_pos = right_pos = result_pos = 0

        while result_pos < len(result):
            if left_pos >= len(left_array) or (right_pos < len(right_array) and self.compare(right_array[right_pos], left_array[left_pos])):
                result[result_pos] = right_array[right_pos]
                right_pos += 1
            else:
                result[result_pos] = left_array[left_pos]
                left_pos += 1

            result_pos += 1

        return result
