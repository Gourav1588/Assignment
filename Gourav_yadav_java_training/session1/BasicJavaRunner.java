package Gourav_yadav_java_training.session1;

import java.util.Scanner;

public class BasicJavaRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        CompareDemo demo = new CompareDemo();

        handleArea(scanner);
        handleMath(scanner);
        handlePatterns(scanner);
         demo.showComparison();

        scanner.close();
    }

    // ================= AREA HANDLING =================
    private static void handleArea(Scanner scanner) {
        AreaCalculator areaCalc = new AreaCalculator();

        System.out.println("\n=== Area Calculator ===");
        System.out.println("Select Shape: 1. Circle 2. Rectangle 3. Triangle");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input. Please enter a number.");
            scanner.next(); 
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter radius: ");
                double radius = scanner.nextDouble();
                System.out.println("Area: " + areaCalc.calculateCircleArea(radius));
                break;

            case 2:
                System.out.print("Enter length and width: ");
                double length = scanner.nextDouble();
                double width = scanner.nextDouble();
                System.out.println("Area: " + areaCalc.calculateRectangleArea(length, width));
                break;

            case 3:
                System.out.print("Enter base and height: ");
                double base = scanner.nextDouble();
                double height = scanner.nextDouble();
                System.out.println("Area: " + areaCalc.calculateTriangleArea(base, height));
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }

    // ================= MATH OPERATIONS =================
    private static void handleMath(Scanner scanner) {
        MathOperations mathOps = new MathOperations();

        System.out.println("\n=== Math Operations ===");

        // Even/Odd
        System.out.print("Enter number to check Even/Odd: ");
        if (scanner.hasNextInt()) {
            int num = scanner.nextInt();
            System.out.println(num + " is " + (mathOps.isEven(num) ? "Even" : "Odd"));
        } else {
            System.out.println("Invalid input.");
            scanner.next();
        }

        // Factorial
        System.out.print("\nEnter number for Factorial: ");
        if (scanner.hasNextInt()) {
            int factNum = scanner.nextInt();
            if (factNum < 0) {
                System.out.println("Factorial not defined for negative numbers.");
            } else {
                System.out.println("Factorial: " + mathOps.findFactorial(factNum));
            }
        } else {
            System.out.println("Invalid input.");
            scanner.next();
        }

        // Fibonacci
        System.out.print("\nEnter Fibonacci limit: ");
        if (scanner.hasNextInt()) {
            int limit = scanner.nextInt();
            mathOps.printFibonacci(limit);
        } else {
            System.out.println("Invalid input.");
            scanner.next();
        }
    }

    // ================= PATTERN PRINTING =================
    private static void handlePatterns(Scanner scanner) {
        PatternPrinter printer = new PatternPrinter();

        System.out.println("\n=== Pattern Printing ===");

        System.out.print("Enter number of rows: ");
        if (scanner.hasNextInt()) {
            int rows = scanner.nextInt();

            if (rows <= 0) {
                System.out.println("Rows must be positive.");
                return;
            }

            System.out.println("\nTriangle Pattern:");
            printer.printTriangle(rows);

            System.out.println("\nSquare Pattern:");
            printer.printSquare(rows);
        } else {
            System.out.println("Invalid input.");
            scanner.next();
        }
    }
}