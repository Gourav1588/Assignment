package Gourav_yadav_java_training.session1.Basic_Operation;


public class MathOperations {

    // Check if number is even or odd 
    public boolean isEven(int number) {
        return number % 2 == 0;
    }

    // Find factorial of a number 
    public long findFactorial(int n) {
        long result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    // Print Fibonacci sequence up to a specified number 
    public void printFibonacci(int limit) {
        int a = 0, b = 1;
        System.out.print("Fibonacci sequence: ");
        while (a <= limit) {
            System.out.print(a + " ");
            int next = a + b;
            a = b;
            b = next;
        }
        System.out.println();
    }
}
