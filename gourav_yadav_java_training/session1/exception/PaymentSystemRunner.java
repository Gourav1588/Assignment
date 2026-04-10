package gourav_yadav_java_training.session1.exception;



import java.util.Scanner;

public class PaymentSystemRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        handlePayment(scanner);

        scanner.close();
    }

    // ================= PAYMENT HANDLER =================
    private static void handlePayment(Scanner scanner) {
        System.out.println("\n=== Payment System ===");

        System.out.print("Enter user name: ");
        String name = scanner.nextLine();

        PaymentSystem user = new PaymentSystem(name);

        // Show role (abstract method implementation)
        user.showRole();

        System.out.print("Enter payment amount: ");

        if (!scanner.hasNextDouble()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        double amount = scanner.nextDouble();

        // Process payment (exception handling inside)
        user.processPayment(amount);
    }
}