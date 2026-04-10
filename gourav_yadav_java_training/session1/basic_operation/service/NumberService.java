package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class NumberService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Number Operations ===");
        System.out.println("1. Check Prime");
        System.out.println("2. Find Largest of 3 Numbers");
        System.out.print("Enter your choice: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {

            case 1:
                handlePrimeCheck(scanner);
                break;

            case 2:
                handleLargest(scanner);
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }

    //  Prime Check (logic inside service)
    private void handlePrimeCheck(Scanner scanner) {
        System.out.print("Enter a number: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int n = scanner.nextInt();

        if (n <= 1) {
            System.out.println(n + " is NOT a Prime number.");
            return;
        }

        boolean isPrime = true;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) {
                isPrime = false;
                break;
            }
        }

        if (isPrime) {
            System.out.println(n + " is a Prime number.");
        } else {
            System.out.println(n + " is NOT a Prime number.");
        }
    }

    //  Largest of 3 (logic inside service)
    private void handleLargest(Scanner scanner) {
        System.out.print("Enter three integers: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }
        int a = scanner.nextInt();

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }
        int b = scanner.nextInt();

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }
        int c = scanner.nextInt();

        int largest;

        if (a >= b && a >= c) {
            largest = a;
        } else if (b >= a && b >= c) {
            largest = b;
        } else {
            largest = c;
        }

        System.out.println("Largest number is: " + largest);
    }
}