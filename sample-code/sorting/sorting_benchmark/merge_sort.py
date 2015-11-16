from sorting_algorithm import SortingAlgorithm


class MergeSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        merge_results = [0] * len(array)
        self.merge_sort_recursive(array, merge_results, 0, len(array) - 1)

    def merge_sort_recursive(self, array, merge_results, left, right):
        if left < right:
            middle = (left + right) // 2
            self.merge_sort_recursive(array, merge_results, left, middle)
            self.merge_sort_recursive(array, merge_results, middle + 1, right)
            self.merge(array, merge_results, left, middle + 1, right)

    def merge(self, array, merge_results, left_begin, right_begin, right_end):
        left_end = right_begin - 1
        left_read_pos = left_begin
        right_read_pos = right_begin
        result_write_pos = left_begin

        while left_read_pos <= left_end and right_read_pos <= right_end:
            if self.compare(array[left_read_pos], array[right_read_pos]):
                merge_results[result_write_pos] = array[left_read_pos]
                left_read_pos += 1
            else:
                merge_results[result_write_pos] = array[right_read_pos]
                right_read_pos += 1
            result_write_pos += 1

        while left_read_pos <= left_end:
            merge_results[result_write_pos] = array[left_read_pos]
            left_read_pos += 1
            result_write_pos += 1

        while right_read_pos <= right_end:
            merge_results[result_write_pos] = array[right_read_pos]
            right_read_pos += 1
            result_write_pos += 1

        array[left_begin:right_end + 1] = merge_results[left_begin:right_end + 1]
