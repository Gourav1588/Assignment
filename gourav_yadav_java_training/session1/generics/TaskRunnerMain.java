package gourav_yadav_java_training.session1.generics;

public class TaskRunnerMain {

    public static void main(String[] args) throws InterruptedException {

        System.out.println("=== Multithreading Demo ===\n");

        // Creating 3 threads running concurrently
        TaskRunner task1 = new TaskRunner("Download File");
        TaskRunner task2 = new TaskRunner("Send Email");
        TaskRunner task3 = new TaskRunner("Generate Report");

        // Start all threads
        task1.start();
        task2.start();
        task3.start();

        // Wait for all to finish
        task1.join();
        task2.join();
        task3.join();

        System.out.println("\nAll tasks completed!");
    }
}