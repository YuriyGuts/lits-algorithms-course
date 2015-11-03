from sorting_algorithm import SortingAlgorithm


class HeapSortAlgorithm(SortingAlgorithm):
    def sort(self, array):
        # Pushing the items one by one into the heap,
        # then retrieving them one by one in the sorted order (the heap guarantees the ordering).
        heap = BinaryHeap(self.compare)
        for item in array:
            heap.add(item)

        result = []
        while heap.size() > 0:
            result.append(heap.remove_top())

        array[:] = result[:]


class BinaryHeap:
    def __init__(self, comparator=None):
        # We can imagine the heap as a binary tree, but for efficiency we'll store the items in a flat array,
        # and compute the indexes of parent / left child / right child using simple O(1) formulas.
        self._items = []
        self._comparator = comparator if comparator is not None else lambda a, b: a < b

    def add(self, item):
        # Adding the item to the right edge of the lowest level of the heap and trying to promote it..
        self._items.append(item)
        self._bubble_up(len(self._items) - 1)

    def peek(self):
        return self._items[0]

    def remove_top(self):
        # Removing the root, replacing the root with the rightmost item on the lowest level and sinking it down.
        self._swap(0, len(self._items) - 1)
        result = self._items.pop()
        self._bubble_down(0)

        # Returning the root that was removed.
        return result

    def size(self):
        return len(self._items)

    def _bubble_up(self, index):
        while self._compare_and_swap_with_parent_if_necessary(index):
            index = self._parent_index(index)

    def _bubble_down(self, index):
        if not self._has_children(index):
            return

        best_child_index = self._best_child_index(index)
        if self._compare_and_swap_with_parent_if_necessary(best_child_index):
            self._bubble_down(best_child_index)

    def _parent_index(self, index):
        return (index - 1) // 2

    def _left_child_index(self, index):
        return index * 2 + 1

    def _right_child_index(self, index):
        return index * 2 + 2

    def _has_children(self, index):
        return self._item_exists(self._left_child_index(index))

    def _item_exists(self, index):
        return 0 <= index < len(self._items)

    def _compare_and_swap_with_parent_if_necessary(self, child_index):
        parent_index = self._parent_index(child_index)
        if not self._item_exists(parent_index):
            return False

        if self._better_item_index(child_index, parent_index) == child_index:
            self._swap(child_index, parent_index)
            return True

        return False

    def _better_item_index(self, index1, index2):
        item1_is_better = self._comparator(self._items[index1], self._items[index2])
        return index1 if item1_is_better else index2

    def _best_child_index(self, parent_index):
        left_child_index = self._left_child_index(parent_index)
        right_child_index = self._right_child_index(parent_index)

        if self._item_exists(left_child_index) and self._item_exists(right_child_index):
            return self._better_item_index(left_child_index, right_child_index)

        return left_child_index

    def _swap(self, index1, index2):
        self._items[index1], self._items[index2] = self._items[index2], self._items[index1]
