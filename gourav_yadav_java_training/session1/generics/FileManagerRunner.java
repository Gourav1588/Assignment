package gourav_yadav_java_training.session1.generics;

import java.util.Scanner;

public class FileManagerRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("\n=== File I/O System ===");
        System.out.print("Enter file name (e.g. output.txt): ");
        String fileName = scanner.nextLine();

        FileManager fm = new FileManager();
        fm.performFileIO(fileName);

        scanner.close();
    }
}