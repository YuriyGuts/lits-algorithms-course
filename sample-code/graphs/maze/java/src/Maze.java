import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Maze {

    private int width;

    private int height;

    private Cell[][] cells;

    private int[][] stepsToReachNeighbors = {
            // x increment, y increment
            {  0, -1 },  // North
            { +1,  0 },  // East
            {  0, +1 },  // South
            { -1,  0 }   // West
    };

    public Maze(int width, int height) {
        this.width = width;
        this.height = height;
        this.cells = new Cell[height][width];

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                this.cells[y][x] = new Cell(x, y, Arrays.asList(true, true, true, true));
            }
        }
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public Cell getCellByCoordinate(int x, int y) {
        return cells[y][x];
    }

    public List<Cell> getAdjacentCells(Cell cell) {
        // Return each of the [N, E, S, W] neighbors as long as they don't cross the maze boundaries.
        List<Cell> neighbors = new ArrayList<>();
        for (int[] step: stepsToReachNeighbors) {
            int neighborX = cell.getX() + step[0];
            int neighborY = cell.getY() + step[1];

            if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                neighbors.add(getCellByCoordinate(neighborX, neighborY));
            }
        }
        return neighbors;
    }

    public List<Cell> getAdjacentReachableCells(Cell cell) {
        // Return each of the [N, E, S, W] neighbors as long as there's no wall between us and the neighbor.
        return getAdjacentCells(cell).stream()
                .filter((neighbor) -> !existsWallBetweenCells(cell, neighbor))
                .collect(Collectors.toList());
    }

    public Boolean existsWallBetweenCells(Cell c1, Cell c2) {
        for (int stepType = 0; stepType < stepsToReachNeighbors.length; stepType++) {
            if (c1.hasWall(stepType)
                    && c1.getX() + stepsToReachNeighbors[stepType][0] == c2.getX()
                    && c1.getY() + stepsToReachNeighbors[stepType][1] == c2.getY()) {
                return true;
            }
        }
        return false;
    }

    public void breakWallBetweenCells(Cell c1, Cell c2) {
        // Each cell maintains its own list of walls, so we need to break them symmetrically.
        // E.g., if we break the southern wall of cell 1, we also need to break the northern wall of cell 2.
        for (int stepType = 0; stepType < stepsToReachNeighbors.length; stepType++) {
            if (c1.getX() + stepsToReachNeighbors[stepType][0] == c2.getX()
                    && c1.getY() + stepsToReachNeighbors[stepType][1] == c2.getY()) {
                c1.breakWall(stepType);
            }
            if (c2.getX() + stepsToReachNeighbors[stepType][0] == c1.getX()
                    && c2.getY() + stepsToReachNeighbors[stepType][1] == c1.getY()) {
                c2.breakWall(stepType);
            }
        }
    }
}
