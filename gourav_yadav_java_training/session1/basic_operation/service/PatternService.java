package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class PatternService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Pattern Printing ===");
        System.out.println("1. Triangle Pattern");
        System.out.println("2. Square Pattern");
        System.out.print("Enter your choice: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        System.out.print("Enter number of rows/size: ");
        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int n = scanner.nextInt();

        if (n <= 0) {
            System.out.println("Value must be positive.");
            return;
        }

        switch (choice) {

            case 1:
                printTriangle(n);
                break;

            case 2:
                printSquare(n);
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }

    private void printTriangle(int rows) {
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    private void printSquare(int size) {
        for (int i = 1; i <= size; i++) {
            for (int j = 1; j <= size; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }
}