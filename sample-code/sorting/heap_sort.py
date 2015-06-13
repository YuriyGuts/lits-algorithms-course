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

        return result


class BinaryHeap:
    def __init__(self, comparator=None):
        # We can imagine the heap as a binary tree, but for efficiency we'll store the items in a flat array,
        # and compute the indexes of parent / left child / right child using simple O(1) formulas.
        self._items = []
        self._comparator = comparator if comparator is not None else lambda a, b: a > b

    def add(self, item):
        # Adding the item to the right edge of the lowest level of the heap and trying to promote it..
        self._items.append(item)
        self._bubble_up(len(self._items) - 1)

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
        parent_index = self._parent_index(index)

        # While the child is better than the parent, swapping them and trying to push the child even higher.
        while self._item_exists(parent_index) and self._comparator(self._items[parent_index], self._items[index]):
            self._swap(index, parent_index)
            index = parent_index
            parent_index = self._parent_index(parent_index)

    def _bubble_down(self, index):
        while True:
            left_index = self._left_index(index)
            right_index = self._right_index(index)

            # If the item is on the lowest level, there's no point to bubble it down further.
            if not self._item_exists(left_index):
                break

            # If there's only the left child that exists, remembering it as the best child.
            if not self._item_exists(right_index):
                better_child_index = left_index
            # Otherwise, comparing the children and remembering which one is better (better=larger for the max-heap).
            else:
                right_is_better = self._comparator(self._items[left_index], self._items[right_index])
                better_child_index = right_index if right_is_better else left_index

            # If the parent is worse than the better child, swapping them and trying to sink the parent even further.
            parent_is_better = self._comparator(self._items[better_child_index], self._items[index])
            if not parent_is_better:
                self._swap(index, better_child_index)
                index = better_child_index
            # Otherwise, it means that the parent is low enough and there's no need to sink it further.
            else:
                break

    def _parent_index(self, index):
        return (index - 1) // 2

    def _left_index(self, index):
        return index * 2 + 1

    def _right_index(self, index):
        return index * 2 + 2

    def _item_exists(self, index):
        return 0 <= index < len(self._items)

    def _swap(self, index1, index2):
        self._items[index1], self._items[index2] = self._items[index2], self._items[index1]
