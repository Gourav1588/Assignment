package gourav_yadav_java_training.session1.basic_operation.service;

import java.util.Scanner;

public class TemperatureService {

    public void process(Scanner scanner) {

        System.out.println("\n=== Temperature Converter ===");
        System.out.println("1. Celsius to Fahrenheit");
        System.out.println("2. Fahrenheit to Celsius");
        System.out.print("Enter your choice: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int choice = scanner.nextInt();

        switch (choice) {

            case 1:
                handleCelsiusToFahrenheit(scanner);
                break;

            case 2:
                handleFahrenheitToCelsius(scanner);
                break;

            default:
                System.out.println("Invalid choice.");
        }
    }

    private void handleCelsiusToFahrenheit(Scanner scanner) {
        System.out.print("Enter temperature in Celsius: ");

        if (!scanner.hasNextDouble()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        double celsius = scanner.nextDouble();
        double result = (celsius * 9 / 5) + 32;

        System.out.println("Fahrenheit: " + result);
    }

    private void handleFahrenheitToCelsius(Scanner scanner) {
        System.out.print("Enter temperature in Fahrenheit: ");

        if (!scanner.hasNextDouble()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        double fahrenheit = scanner.nextDouble();
        double result = (fahrenheit - 32) * 5 / 9;

        System.out.println("Celsius: " + result);
    }
}