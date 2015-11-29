import javax.swing.*;
import javax.swing.border.Border;
import java.awt.*;
import java.lang.reflect.InvocationTargetException;

public class Program {

    private static final int mazeWidth = 40;
    private static final int mazeHeight = 25;
    private static final int mazeCellSize = 25;
    private static final long animationDelayMillis = 10;

    private static MazeGenerator mazeGenerator;

    private static JFrame window;
    private static MazePanel mazePanel;
    private static JButton goButton;

    public static void main(String[] args)
    {
        mazeGenerator = new MazeGenerator(mazeWidth, mazeHeight);
        SwingUtilities.invokeLater(Program::createAndShowGUI);
    }

    private static void createAndShowGUI()
    {
        mazePanel = new MazePanel(mazeCellSize);
        mazePanel.setMaze(mazeGenerator.getMaze());

        JFrame.setDefaultLookAndFeelDecorated(true);
        window = new JFrame("Maze Algorithms");

        JPanel containerPanel = new JPanel();
        containerPanel.setLayout(new BoxLayout(containerPanel, BoxLayout.PAGE_AXIS));
        containerPanel.setBorder(BorderFactory.createEmptyBorder(30, 30, 30, 30));

        goButton = new JButton("Go!");
        goButton.addActionListener(e -> onGoButtonClick());
        goButton.setActionCommand("Go");
        goButton.setAlignmentX(Component.CENTER_ALIGNMENT);

        containerPanel.add(goButton);
        containerPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        containerPanel.add(mazePanel);

        window.pack();
        window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        window.getContentPane().add(containerPanel);
        window.setSize(window.getPreferredSize());
        window.setResizable(false);
        window.setLocationRelativeTo(null);
        window.setVisible(true);
    }

    private static void onGoButtonClick() {
        mazeGenerator = new MazeGenerator(mazeWidth, mazeHeight);
        mazePanel.setMaze(mazeGenerator.getMaze());

        new Thread(() -> {
            SwingUtilities.invokeLater(() -> goButton.setEnabled(false));
            mazeGenerator.generate(Program::onCellCreated);
            SwingUtilities.invokeLater(() -> goButton.setEnabled(true));
        }).start();
    }

    private static void onCellCreated(CellCreatedEvent e) {
        try {
            Thread.sleep(animationDelayMillis);
            SwingUtilities.invokeAndWait(() -> window.repaint());
        } catch (InterruptedException | InvocationTargetException ex) {
            ex.printStackTrace();
        }
    }
}
