import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

// A naive implementation of Union-Find using a flat array with leader pointers.
public class ArrayUnionFind extends UnionFind {

    private class UnionFindGroup {
        public UnionFindItem leader;
        public List<UnionFindItem> items = new ArrayList<>();

        public UnionFindGroup(UnionFindItem leader) {
            this.leader = leader;
        }

        @Override
        public String toString() {
            return String.format("Leader: %d  Items: %s",
                    leader.value,
                    items.stream().map(i -> String.valueOf(i.value)).collect(Collectors.joining(", "))
            );
        }
    }

    private class UnionFindItem {
        public int value;
        public UnionFindGroup group;

        public UnionFindItem(int value, UnionFindGroup group) {
            this.value = value;
            this.group = group;
        }

        @Override
        public String toString() {
            return String.format("Value: %d", value);
        }
    }

    private UnionFindItem[] items;
    private List<UnionFindGroup> groups;

    public ArrayUnionFind(int capacity) {
        super(capacity);
        items = new UnionFindItem[capacity];
        groups = new ArrayList<>(capacity);
    }

    @Override
    public int insert(int value) {
        // Creating a separate disconnected group with one item.
        UnionFindItem newItem = new UnionFindItem(value, null);
        UnionFindGroup newGroup = new UnionFindGroup(newItem);

        items[value] = newItem;
        newGroup.items.add(newItem);
        groups.add(newGroup);
        newItem.group = newGroup;

        return find(value);
    }

    @Override
    public int union(int value1, int value2) {
        UnionFindGroup group1 = findGroup(value1);
        UnionFindGroup group2 = findGroup(value2);

        // If already merged, return group name for any of the two items.
        if (group1.leader.value == group2.leader.value) {
            return group1.leader.value;
        }

        // If we got here, then both items are present and disjoint: perform a normal union.
        UnionFindGroup greaterGroup = group1.items.size() > group2.items.size() ? group1 : group2;
        UnionFindGroup lesserGroup = greaterGroup == group1 ? group2 : group1;

        // Updating leader pointers on the lesser group.
        for (UnionFindItem item: lesserGroup.items) {
            item.group = greaterGroup;
            greaterGroup.items.add(item);
        }

        // Removing the merged group.
        groups.remove(lesserGroup);
        return greaterGroup.leader.value;
    }

    @Override
    public int find(int value) {
        return findGroup(value).leader.value;
    }

    private UnionFindGroup findGroup(int value) {
        return items[value].group;
    }
}
