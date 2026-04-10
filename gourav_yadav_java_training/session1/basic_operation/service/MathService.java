package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class MathService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Math Operations ===");
        System.out.println("1. Even / Odd Check");
        System.out.println("2. Factorial");
        System.out.println("3. Fibonacci");
        System.out.print("Enter your choice: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {

            case 1:
                handleEvenOdd(scanner);
                break;

            case 2:
                handleFactorial(scanner);
                break;

            case 3:
                handleFibonacci(scanner);
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }

    private void handleEvenOdd(Scanner scanner) {
        System.out.print("Enter a number: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int number = scanner.nextInt();

        if (number % 2 == 0) {
            System.out.println(number + " is Even");
        } else {
            System.out.println(number + " is Odd");
        }
    }

    private void handleFactorial(Scanner scanner) {
        System.out.print("Enter a number: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int n = scanner.nextInt();

        if (n < 0) {
            System.out.println("Factorial not defined for negative numbers.");
            return;
        }

        long result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }

        System.out.println("Factorial: " + result);
    }

    private void handleFibonacci(Scanner scanner) {
        System.out.print("Enter limit: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int limit = scanner.nextInt();

        int a = 0, b = 1;

        System.out.print("Fibonacci sequence: ");
        while (a <= limit) {
            System.out.print(a + " ");
            int next = a + b;
            a = b;
            b = next;
        }
        System.out.println();
    }
}