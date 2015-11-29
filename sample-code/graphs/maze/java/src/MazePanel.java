import javax.swing.*;
import java.awt.*;

public class MazePanel extends JPanel {

    private Maze maze;

    private int mazeCellSize;

    private int[][] wallTemplates = new int[][] {
            // x1, y1, x2, y2
            { 0, 0, 1, 0 },  // N
            { 1, 0, 1, 1 },  // E
            { 0, 1, 1, 1 },  // S
            { 0, 0, 0, 1 }   // W
    };

    public MazePanel(int mazeCellSize) {
        this.mazeCellSize = mazeCellSize;
        this.setBackground(Color.lightGray);
    }

    public void setMaze(Maze maze) {
        this.maze = maze;
        repaint();
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(maze.getWidth() * mazeCellSize + 1, maze.getHeight() * mazeCellSize + 1);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        for (int y = 0; y < maze.getHeight(); y++) {
            for (int x = 0; x < maze.getWidth(); x++) {
                Cell cell = maze.getCellByCoordinate(x, y);
                if (!cell.hasAllWalls()) {
                    paintCell(cell, g);
                }
            }
        }
    }

    private void paintCell(Cell cell, Graphics g) {
        g.setColor(Color.white);
        g.fillRect(cell.getX() * mazeCellSize, cell.getY() * mazeCellSize, mazeCellSize, mazeCellSize);

        g.setColor(Color.black);
        for (int w = 0; w < cell.getWalls().size(); w++) {
            if (cell.hasWall(w)) {
                g.drawLine(
                        mazeCellSize * (cell.getX() + wallTemplates[w][0]),
                        mazeCellSize * (cell.getY() + wallTemplates[w][1]),
                        mazeCellSize * (cell.getX() + wallTemplates[w][2]),
                        mazeCellSize * (cell.getY() + wallTemplates[w][3])
                );
            }
        }
    }
}
