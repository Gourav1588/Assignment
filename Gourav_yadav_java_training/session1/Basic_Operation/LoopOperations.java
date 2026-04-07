package Gourav_yadav_java_training.session1.Basic_Operation;



public class LoopOperations {

   
    public void printMultiplicationTable(int n) {
        System.out.println("Multiplication Table for " + n + ":");
        for (int i = 1; i <= 10; i++) {
            System.out.println(n + " x " + i + " = " + (n * i));
        }
    }

    
    public int sumOfEvensToTen() {
        int sum = 0;
        int i = 1;
        while (i <= 10) {
            if (i % 2 == 0) {
                sum += i;
            }
            i++;
        }
        return sum;
    }
}
