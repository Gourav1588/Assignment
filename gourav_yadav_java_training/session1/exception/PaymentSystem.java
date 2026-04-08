package gourav_yadav_java_training.session1.exception;


// Interface defining a contract 
interface Payable {
    void processPayment(double amount);
}

// Abstract Class providing partial implementation 
abstract class User {
     String name;
    User(String name) { this.name = name; }
    abstract void showRole();
}

// Concrete class implementing both 
public class PaymentSystem extends User implements Payable {
    public PaymentSystem(String name) { super(name); }

    @Override
    public void showRole() { System.out.println("User: " + name); }

    @Override
    public void processPayment(double amount) {
        try { // Handling potential exceptions 
            if (amount <= 0) throw new IllegalArgumentException("Amount must be positive.");
            System.out.println("Processing payment of " + amount);
        } catch (IllegalArgumentException e) {
            System.out.println("Caught Exception: " + e.getMessage());
        }
    }
}
