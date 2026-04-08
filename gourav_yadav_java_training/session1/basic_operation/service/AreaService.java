package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class AreaService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Area Calculator ===");
        System.out.println("1. Circle");
        System.out.println("2. Rectangle");
        System.out.println("3. Triangle");
        System.out.print("Enter your choice: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input. Please enter a number.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {

            case 1:
                System.out.print("Enter radius: ");
                if (scanner.hasNextDouble()) {
                    double radius = scanner.nextDouble();
                    double area = Math.PI * radius * radius;
                    System.out.println("Area of Circle: " + area);
                } else {
                    System.out.println("Invalid input.");
                    scanner.next();
                }
                break;

            case 2:
                System.out.print("Enter length and width: ");
                if (scanner.hasNextDouble()) {
                    double length = scanner.nextDouble();

                    if (scanner.hasNextDouble()) {
                        double width = scanner.nextDouble();
                        double area = length * width;
                        System.out.println("Area of Rectangle: " + area);
                    } else {
                        System.out.println("Invalid width.");
                        scanner.next();
                    }

                } else {
                    System.out.println("Invalid length.");
                    scanner.next();
                }
                break;

            case 3:
                System.out.print("Enter base and height: ");
                if (scanner.hasNextDouble()) {
                    double base = scanner.nextDouble();

                    if (scanner.hasNextDouble()) {
                        double height = scanner.nextDouble();
                        double area = 0.5 * base * height;
                        System.out.println("Area of Triangle: " + area);
                    } else {
                        System.out.println("Invalid height.");
                        scanner.next();
                    }

                } else {
                    System.out.println("Invalid base.");
                    scanner.next();
                }
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }
}