package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class OperatorService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Operator Demonstration ===");

        System.out.print("Enter value for a: ");
        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }
        int a = scanner.nextInt();

        System.out.print("Enter value for b: ");
        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }
        int b = scanner.nextInt();

        runDemo(a, b);
    }

    private void runDemo(int a, int b) {

        System.out.println("\n=== Arithmetic Operators ===");
        System.out.println("a + b = " + (a + b));
        System.out.println("a - b = " + (a - b));
        System.out.println("a * b = " + (a * b));

        if (b != 0) {
            System.out.println("a / b = " + (a / b));
            System.out.println("a % b = " + (a % b));
        } else {
            System.out.println("Division and modulus not allowed when b = 0");
        }

        System.out.println("\n=== Relational Operators ===");
        System.out.println("a > b  : " + (a > b));
        System.out.println("a < b  : " + (a < b));
        System.out.println("a >= b : " + (a >= b));
        System.out.println("a <= b : " + (a <= b));
        System.out.println("a == b : " + (a == b));
        System.out.println("a != b : " + (a != b));

        System.out.println("\n=== Logical Operators ===");

        boolean bothPositive = (a > 0 && b > 0);
        boolean eitherPositive = (a > 0 || b > 0);
        boolean aNotPositive = !(a > 0);

        System.out.println("Both a and b are positive? " + bothPositive);
        System.out.println("Either a or b is positive? " + eitherPositive);
        System.out.println("a is NOT positive? " + aNotPositive);
    }
}