import javax.swing.*;
import java.awt.*;
import java.lang.reflect.InvocationTargetException;

public class Program {

    private static final int mazeWidth = 40;
    private static final int mazeHeight = 25;
    private static final int mazeCellSize = 25;
    private static final long animationDelayMillis = 10;

    private static MazeGenerator mazeGenerator;
    private static MazeSolver mazeSolver;

    private static JFrame window;
    private static MazePanel mazePanel;
    private static JButton goButton;

    public static void main(String[] args)
    {
        mazeGenerator = new MazeGenerator(mazeWidth, mazeHeight);
        mazeSolver = new MazeSolver();
        SwingUtilities.invokeLater(Program::createAndShowGUI);
    }

    private static void createAndShowGUI()
    {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (ClassNotFoundException | InstantiationException | UnsupportedLookAndFeelException | IllegalAccessException e) {
            e.printStackTrace();
        }

        JFrame.setDefaultLookAndFeelDecorated(true);
        window = new JFrame("Maze Algorithms");

        JPanel containerPanel = new JPanel();
        containerPanel.setLayout(new BoxLayout(containerPanel, BoxLayout.PAGE_AXIS));
        containerPanel.setBorder(BorderFactory.createEmptyBorder(30, 30, 30, 30));

        goButton = new JButton("Go!");
        goButton.addActionListener(e -> onGoButtonClick());
        goButton.setActionCommand("Go");
        goButton.setAlignmentX(Component.CENTER_ALIGNMENT);

        mazePanel = new MazePanel(mazeWidth, mazeHeight, mazeCellSize);

        containerPanel.add(goButton);
        containerPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        containerPanel.add(mazePanel);

        window.setResizable(false);
        window.getContentPane().add(containerPanel);
        window.pack();
        window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        window.setSize(window.getPreferredSize());
        window.setLocationRelativeTo(null);
        window.setVisible(true);
    }

    private static void onGoButtonClick() {
        mazeGenerator = new MazeGenerator(mazeWidth, mazeHeight);
        mazePanel.clear();

        new Thread(() -> {
            SwingUtilities.invokeLater(() -> goButton.setEnabled(false));
            Maze maze = mazeGenerator.generate(Program::onCellCreated);
            MazeSolution solution = mazeSolver.solve(maze, Program::onCellSolved, Program::onExitPathUpdated);
            SwingUtilities.invokeLater(() -> goButton.setEnabled(true));
        }).start();
    }

    private static void onCellCreated(CellCreatedEvent e) {
        executeWithAnimationDelay(() -> {
            mazePanel.addGeneratedCell(e.getTraversalItem().getPreviousCell());
            mazePanel.addGeneratedCell(e.getTraversalItem().getCurrentCell());
        });
    }

    private static void onCellSolved(CellSolvedEvent e) {
        executeWithAnimationDelay(() -> {
            Cell cell = e.getTraversalItem().getCell();
            int pathLength = e.getTraversalItem().getMinPathLength();
            mazePanel.addSolvedCell(cell, pathLength);
        });
    }

    private static void onExitPathUpdated(ExitPathUpdatedEvent e) {
        executeWithAnimationDelay(() -> {
            mazePanel.addExitPathCell(e.getCell());
        });
    }

    private static void executeWithAnimationDelay(Runnable function) {
        try {
            function.run();
            Thread.sleep(animationDelayMillis);
            SwingUtilities.invokeAndWait(() -> window.repaint());
        } catch (InterruptedException | InvocationTargetException ex) {
            ex.printStackTrace();
        }
    }
}
