public abstract class UnionFind {

    private int capacity;

    public UnionFind(int capacity) {
        this.capacity = capacity;
    }

    public abstract int insert(int value);

    public abstract int union(int value1, int value2);

    public abstract int find(int value);
}
