class ArrayUnionFind:
    """A naive implementation of Union-Find using a flat array with leader pointers."""

    class UnionFindGroup:
        def __init__(self, leader):
            self.leader = leader
            self.items = [leader]

    class UnionFindItem:
        def __init__(self, value, group):
            self.value = value
            self.group = group

    def __init__(self, capacity):
        self.groups = []
        self.items = [None] * capacity

    def insert(self, value):
        # Creating a separate disconnected group with one item.
        new_item = self.UnionFindItem(value, None)
        new_group = self.UnionFindGroup(new_item)
        new_item.group = new_group
        self.items[value] = new_item
        self.groups.append(new_group)
        return self.find(value)

    def union(self, value1, value2):
        group1 = self.find(value1)
        group2 = self.find(value2)

        # If already merged, return group name for any of the two items.
        if group1.leader == group2.leader:
            return self.find(value1)

        # If we got here, then both items are present and disjoint: perform a normal union.
        greater_group = group1
        lesser_group = group2
        if len(group1.items) < len(group2.items):
            lesser_group = group1
            greater_group = group2

        # Updating leader pointers on the lesser group.
        for item in lesser_group.items:
            item.group = greater_group
            greater_group.items.append(item)

        # Removing the merged group.
        self.groups.remove(lesser_group)
        return self.find(value1)

    def find(self, item1):
        if self.items[item1] is None:
            return None
        return self.items[item1].group

    def group_count(self):
        return len(self.groups)
