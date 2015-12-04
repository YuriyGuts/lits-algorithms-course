public class ExitPathUpdatedEvent {

    private Cell cell;

    public ExitPathUpdatedEvent(Cell cell) {
        this.cell = cell;
    }

    public Cell getCell() {
        return cell;
    }
}
