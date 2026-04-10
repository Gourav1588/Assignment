package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class LoopService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Loop Operations ===");
        System.out.println("1. Multiplication Table");
        System.out.println("2. Sum of Even Numbers (1 to 10)");
        System.out.print("Enter your choice: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {

            case 1:
                handleMultiplicationTable(scanner);
                break;

            case 2:
                handleSumOfEvens();
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }

    // Multiplication Table
    private void handleMultiplicationTable(Scanner scanner) {
        System.out.print("Enter a number: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int n = scanner.nextInt();

        System.out.println("Multiplication Table for " + n + ":");
        for (int i = 1; i <= 10; i++) {
            System.out.println(n + " x " + i + " = " + (n * i));
        }
    }

    // Sum of Even Numbers
    private void handleSumOfEvens() {
        int sum = 0;
        int i = 1;

        while (i <= 10) {
            if (i % 2 == 0) {
                sum += i;
            }
            i++;
        }

        System.out.println("Sum of even numbers from 1 to 10 is: " + sum);
    }
}