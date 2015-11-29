import java.util.Arrays;
import java.util.List;

public class Cell {

    private int x;

    private int y;

    private List<Boolean> walls;

    public Cell(int x, int y, List<Boolean> walls) {
        this.x = x;
        this.y = y;
        this.walls = walls;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public List<Boolean> getWalls() {
        return walls;
    }

    public void breakWall(int wallIndex) {
        walls.set(wallIndex, false);
    }

    public boolean hasWall(int wallIndex) {
        return walls.get(wallIndex);
    }

    public boolean hasAllWalls() {
        return !walls.contains(false);
    }

    @Override
    public String toString() {
        return String.format("x=%d  y=%d  walls=%s", x, y, Arrays.toString(walls.toArray()));
    }
}
