package Gourav_yadav_java_training.session1;

import java.util.Scanner;

public class BasicJavaRunner {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        AreaCalculator areaCalc = new AreaCalculator();
        MathOperations mathOps = new MathOperations();

        System.out.println("--- Area Calculation ---");
        System.out.println("Select Shape: 1. Circle | 2. Rectangle | 3. Triangle");
        System.out.print("Choice: ");
        int choice = scanner.nextInt();

        if (choice == 1) {
            System.out.print("Enter radius: ");
            double radius = scanner.nextDouble();
            System.out.println("Area of Circle: " + areaCalc.calculateCircleArea(radius));
        } else if (choice == 2) {
            System.out.print("Enter length: ");
            double length = scanner.nextDouble();
            System.out.print("Enter width: ");
            double width = scanner.nextDouble();
            System.out.println("Area of Rectangle: " + areaCalc.calculateRectangleArea(length, width));
        } else if (choice == 3) {
            System.out.print("Enter base: ");
            double base = scanner.nextDouble();
            System.out.print("Enter height: ");
            double height = scanner.nextDouble();
            System.out.println("Area of Triangle: " + areaCalc.calculateTriangleArea(base, height));
        } else {
            System.out.println("Invalid choice for Area Calculator.");
        }

        // Testing Even/Odd
        System.out.print("\nEnter number to check Even/Odd: ");
        int num = scanner.nextInt();
        System.out.println(num + " is " + (mathOps.isEven(num) ? "Even" : "Odd"));

        // Testing Factorial
        System.out.print("\nEnter number for Factorial: ");
        System.out.println("Factorial: " + mathOps.findFactorial(scanner.nextInt()));

        // Testing Fibonacci
        System.out.print("\nEnter Fibonacci limit: ");
        mathOps.printFibonacci(scanner.nextInt());

        scanner.close();
    }
}