package Gourav_yadav_java_training.session1.Basic_Operation;

import java.util.Scanner;

public class BasicJavaRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        CompareDemo demo = new CompareDemo();
        NumberChecker checker = new NumberChecker();
        LoopOperations loopOps = new LoopOperations();

        handleArea(scanner);
        handleMath(scanner);
        handlePatterns(scanner);
        demo.showComparison();
        handleOperatorDemo(scanner);
        handleTemperatureConversion(scanner);
        handlePrimeCheck(scanner, checker);
        handleLargestNumber(scanner, checker);
         handleMultiplicationTable(scanner, loopOps);
        handleSumOfEvens(loopOps);

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


     // ================= OPERATOR DEMO HANDLER =================
    private static void handleOperatorDemo(Scanner scanner) {
        OperatorDemo demo = new OperatorDemo();

        System.out.println("\n=== Operator Demonstration ===");

        // Input for a
        System.out.print("Enter value for a: ");
        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input for a.");
            scanner.next(); // clear invalid input
            return;
        }
        int a = scanner.nextInt();

        // Input for b
        System.out.print("Enter value for b: ");
        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input for b.");
            scanner.next(); // clear invalid input
            return;
        }
        int b = scanner.nextInt();

        // Running  demo
        demo.runDemo(a, b);
    }


     // ================= TEMPERATURE CONVERSION HANDLER =================
    private static void handleTemperatureConversion(Scanner scanner) {
        TempConverter converter = new TempConverter();

        System.out.println("\n=== Temperature Converter ===");
        System.out.println("Choose conversion type:");
        System.out.println("1. Celsius to Fahrenheit");
        System.out.println("2. Fahrenheit to Celsius");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid choice.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter temperature in Celsius: ");
                if (scanner.hasNextDouble()) {
                    double celsius = scanner.nextDouble();
                    double result = converter.toFahrenheit(celsius);
                    System.out.println("Fahrenheit: " + result);
                } else {
                    System.out.println("Invalid input.");
                    scanner.next();
                }
                break;

            case 2:
                System.out.print("Enter temperature in Fahrenheit: ");
                if (scanner.hasNextDouble()) {
                    double fahrenheit = scanner.nextDouble();
                    double result = converter.toCelsius(fahrenheit);
                    System.out.println("Celsius: " + result);
                } else {
                    System.out.println("Invalid input.");
                    scanner.next();
                }
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }
     

    // ================= PRIME CHECK =================
    private static void handlePrimeCheck(Scanner scanner, NumberChecker checker) {
        System.out.println("\n=== Prime Number Check ===");
        System.out.print("Enter a number: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int num = scanner.nextInt();

        if (checker.isPrime(num)) {
            System.out.println(num + " is a Prime number.");
        } else {
            System.out.println(num + " is NOT a Prime number.");
        }
    }

    // ================= LARGEST NUMBER =================
    private static void handleLargestNumber(Scanner scanner, NumberChecker checker) {
        System.out.println("\n=== Find Largest of Three Numbers ===");

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

        int largest = checker.findLargest(a, b, c);
        System.out.println("Largest number is: " + largest);
    }

     // ================= MULTIPLICATION TABLE =================
    private static void handleMultiplicationTable(Scanner scanner, LoopOperations loopOps) {
        System.out.println("\n=== Multiplication Table ===");
        System.out.print("Enter a number: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int number = scanner.nextInt();
        loopOps.printMultiplicationTable(number);
    }

    // ================= SUM OF EVEN NUMBERS =================
    private static void handleSumOfEvens(LoopOperations loopOps) {
        System.out.println("\n=== Sum of Even Numbers (1 to 10) ===");

        int sum = loopOps.sumOfEvensToTen();
        System.out.println("Sum of even numbers from 1 to 10 is: " + sum);
    }


}