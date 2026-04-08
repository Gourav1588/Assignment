package gourav_yadav_java_training.session1.basic_operation.service;

public class CompareService {

    public void process() {

        System.out.println("\n=== Comparison Demo ===");

        // ===== PRIMITIVE TYPE EXAMPLE =====
        int a = 10;
        int b = 10;

        System.out.println("Primitive comparison (a == b): " + (a == b));

        // ===== REFERENCE TYPE EXAMPLE =====
        String str1 = new String("Hello");
        String str2 = new String("Hello");

        System.out.println("Reference comparison (str1 == str2): " + (str1 == str2));

        // ===== CORRECT WAY TO COMPARE CONTENT =====
        System.out.println("Using equals() (str1.equals(str2)): " + str1.equals(str2));

        // ===== STRING POOL EXAMPLE =====
        String s1 = "Hello";
        String s2 = "Hello";

        System.out.println("String pool comparison (s1 == s2): " + (s1 == s2));
    }
}