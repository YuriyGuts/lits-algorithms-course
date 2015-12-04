import javax.swing.*;
import java.awt.*;
import java.awt.geom.Rectangle2D;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MazePanel extends JPanel {

    private final Color COLOR_CELL_BACKGROUND = Color.white;
    private final Color COLOR_SOLVED_CELL_BACKGROUND = new Color(204, 229, 255);
    private final Color COLOR_CELL_TEXT = Color.black;
    private final Color COLOR_WALL = Color.black;
    private final Color COLOR_PATH = new Color(128, 0, 0);

    private final Font FONT_CELL_TEXT = new Font("", 0, 9);
    private final Stroke STROKE_WALL = new BasicStroke(1);
    private final Stroke STROKE_PATH = new BasicStroke(3);

    private final RenderingHints FONT_RENDERING_HINTS = new RenderingHints(
            RenderingHints.KEY_TEXT_ANTIALIASING,
            RenderingHints.VALUE_TEXT_ANTIALIAS_GASP
    );

    private int mazeHeight;
    private int mazeWidth;
    private int mazeCellSize;

    private ArrayList<Cell> generatedCells;
    private ArrayList<Cell> solvedCells;
    private ArrayList<Cell> exitPathCells;
    private Map<Cell, String> cellLabels;

    private int[][] wallTemplates = new int[][] {
            // x1, y1, x2, y2
            { 0, 0, 1, 0 },  // Northern
            { 1, 0, 1, 1 },  // Eastern
            { 0, 1, 1, 1 },  // Southern
            { 0, 0, 0, 1 }   // Western
    };

    public MazePanel(int mazeWidth, int mazeHeight, int mazeCellSize) {
        this.mazeWidth = mazeWidth;
        this.mazeHeight = mazeHeight;
        this.mazeCellSize = mazeCellSize;
        this.generatedCells = new ArrayList<>();
        this.solvedCells = new ArrayList<>();
        this.exitPathCells = new ArrayList<>();
        this.cellLabels = new HashMap<>();
        this.setBackground(Color.lightGray);
    }

    public void clear() {
        generatedCells.clear();
        solvedCells.clear();
        exitPathCells.clear();
        cellLabels.clear();
        repaint();
    }

    public void addGeneratedCell(Cell cell) {
        generatedCells.add(cell);
    }

    public void addSolvedCell(Cell cell, int pathLength) {
        solvedCells.add(cell);
        cellLabels.put(cell, String.valueOf(pathLength));
    }

    public void addExitPathCell(Cell cell) {
        exitPathCells.add(cell);
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(mazeWidth * mazeCellSize + 1, mazeHeight * mazeCellSize + 1);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D)g;

        for (Cell generatedCell: new ArrayList<>(generatedCells)) {
            paintCell(g2d, generatedCell, COLOR_CELL_BACKGROUND, null);
        }
        for (Cell solvedCell: new ArrayList<>(solvedCells)) {
            paintCell(g2d, solvedCell, COLOR_SOLVED_CELL_BACKGROUND, cellLabels.get(solvedCell));
        }
        for (int i = 1; i < exitPathCells.size(); i++) {
            paintPathSegment(g2d, exitPathCells.get(i - 1), exitPathCells.get(i));
        }
    }

    private Point getCellUpperLeftPoint(Cell cell) {
        return new Point(cell.getX() * mazeCellSize, cell.getY() * mazeCellSize);
    }

    private Point getCellCenterPoint(Cell cell) {
        Point upperLeftPoint = getCellUpperLeftPoint(cell);
        return new Point(upperLeftPoint.x + mazeCellSize / 2, upperLeftPoint.y + mazeCellSize / 2);
    }

    private void paintCell(Graphics2D g, Cell cell, Color color, String text) {
        Point cellUpperLeft = getCellUpperLeftPoint(cell);
        Point cellCenter = getCellCenterPoint(cell);

        // Paint cell background.
        g.setColor(color);
        g.fillRect(cellUpperLeft.x, cellUpperLeft.y, mazeCellSize, mazeCellSize);

        // Paint text, if specified.
        if (text != null) {
            g.setColor(COLOR_CELL_TEXT);
            g.setFont(FONT_CELL_TEXT);
            g.setRenderingHints(FONT_RENDERING_HINTS);

            Rectangle2D labelBounds = g.getFontMetrics().getStringBounds(text, g);
            g.drawString(text, cellCenter.x - (int)labelBounds.getWidth() / 2, cellCenter.y + (int)labelBounds.getHeight() / 2);
        }

        // Paint walls.
        g.setColor(COLOR_WALL);
        g.setStroke(STROKE_WALL);

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

    private void paintPathSegment(Graphics2D g, Cell startCell, Cell endCell) {
        Point startCellCenter = getCellCenterPoint(startCell);
        Point endCellCenter = getCellCenterPoint(endCell);

        g.setColor(COLOR_PATH);
        g.setStroke(STROKE_PATH);
        g.drawLine(startCellCenter.x, startCellCenter.y, endCellCenter.x, endCellCenter.y);
    }
}
