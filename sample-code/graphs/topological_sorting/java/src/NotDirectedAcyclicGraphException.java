public class NotDirectedAcyclicGraphException extends RuntimeException {

    public NotDirectedAcyclicGraphException() {
        super("The graph is not a directed acyclic graph (DAG).");
    }

}
