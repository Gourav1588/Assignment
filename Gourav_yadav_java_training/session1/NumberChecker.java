package Gourav_yadav_java_training.session1;




public class NumberChecker {
    
    // Q1: Check if a number is prime using if-else
    public boolean isPrime(int n) {
        if (n <= 1) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }

    // Q2: Find the largest among three numbers using conditional statements 
    public int findLargest(int a, int b, int c) {
        if (a >= b && a >= c) {
            return a;
        } else if (b >= a && b >= c) {
            return b;
        } else {
            return c;
        }
    }
}