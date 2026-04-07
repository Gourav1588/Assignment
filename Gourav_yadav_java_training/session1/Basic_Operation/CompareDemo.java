package Gourav_yadav_java_training.session1.Basic_Operation;

  


public class CompareDemo {

    public void showComparison() {

        // ===== PRIMITIVE TYPE EXAMPLE =====
        // Primitive variables store actual values directly in memory (stack)
        int a = 10;
        int b = 10;

        // Comparing actual values → true
        System.out.println("Primitive comparison (a == b): " + (a == b));


        // ===== REFERENCE TYPE EXAMPLE =====
        // "new String()" creates a new object in heap memory every time
        String str1 = new String("Hello");
        String str2 = new String("Hello");

        // Comparing memory addresses → false
        System.out.println("Reference comparison (str1 == str2): " + (str1 == str2));


        // ===== CORRECT WAY TO COMPARE CONTENT =====
        // .equals() compares actual content → true
        System.out.println("Using equals() (str1.equals(str2)): " + str1.equals(str2));


        // ===== STRING POOL EXAMPLE =====
        // Java reuses same object from String Pool
        String s1 = "Hello";
        String s2 = "Hello";

        // Same memory reference → true
        System.out.println("String pool comparison (s1 == s2): " + (s1 == s2));
    }
}