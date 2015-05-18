import java.io.*;
import java.util.Scanner;

public class Alice {
    public static void main(String[] args) throws FileNotFoundException {
    	String content = new Scanner(new File("echoer.in")).useDelimiter("\\Z").next();

    	System.err.println("This is an error");
    	System.out.println("This is some output");

        PrintWriter out = new PrintWriter("echoer.out");
        out.println("Solution: " + content);
        out.close();
    }
}
