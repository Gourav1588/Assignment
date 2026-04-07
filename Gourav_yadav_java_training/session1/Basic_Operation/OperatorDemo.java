package Gourav_yadav_java_training.session1.Basic_Operation;



public class OperatorDemo {

    public void runDemo(int a, int b) {

        // ================= Arithmetic Operators =================
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

        // ================= Relational Operators =================
        System.out.println("\n=== Relational Operators ===");
        System.out.println("a > b  : " + (a > b));
        System.out.println("a < b  : " + (a < b));
        System.out.println("a >= b : " + (a >= b));
        System.out.println("a <= b : " + (a <= b));
        System.out.println("a == b : " + (a == b));
        System.out.println("a != b : " + (a != b));

        // ================= Logical Operators =================
        System.out.println("\n=== Logical Operators ===");

        boolean bothPositive = (a > 0 && b > 0);
        boolean eitherPositive = (a > 0 || b > 0);
        boolean aNotPositive = !(a > 0);

        System.out.println("Both a and b are positive? " + bothPositive);
        System.out.println("Either a or b is positive? " + eitherPositive);
        System.out.println("a is NOT positive? " + aNotPositive);
    }
}
