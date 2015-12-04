import java.util.List;

public class MazeSolution {

    private int[][] pathLengths;

    private List<Cell> exitPath;

    public MazeSolution(int[][] pathLengths, List<Cell> exitPath) {
        this.pathLengths = pathLengths;
        this.exitPath = exitPath;
    }

    public int[][] getPathLengths() {
        return pathLengths;
    }

    public List<Cell> getExitPath() {
        return exitPath;
    }

}
