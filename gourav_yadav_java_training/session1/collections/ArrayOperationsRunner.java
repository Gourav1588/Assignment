package gourav_yadav_java_training.session1.collections;

import java.util.Scanner;
import java.util.Arrays;

public class ArrayOperationsRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayOperations ops = new ArrayOperations();

        int[] arr = readArray(scanner);

        handleAverage(arr, ops);
        handleSorting(arr, ops);
        handleSearch(scanner, arr, ops);

        scanner.close();
    }

    // ================= READ ARRAY =================
    private static int[] readArray(Scanner scanner) {
        System.out.print("Enter number of elements: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            
            scanner.next();
            return new int[0];
        }

        int n = scanner.nextInt();
        int[] arr = new int[n];

        System.out.println("Enter " + n + " elements:");

        for (int i = 0; i < n; i++) {
            if (scanner.hasNextInt()) {
                arr[i] = scanner.nextInt();
            } else {
                System.out.println("Invalid input.");
                scanner.next();
                i--; // retry same index
            }
        }

        return arr;
    }

    // ================= AVERAGE =================
    private static void handleAverage(int[] arr, ArrayOperations ops) {
        System.out.println("\n=== Average Calculation ===");
        double avg = ops.calculateAverage(arr);
        System.out.println("Average: " + avg);
    }

    // ================= SORTING =================
    private static void handleSorting(int[] arr, ArrayOperations ops) {
        System.out.println("\n=== Bubble Sort ===");

        int[] copy = Arrays.copyOf(arr, arr.length); // preserve original
        ops.bubbleSort(copy);

        System.out.println("Sorted Array: " + Arrays.toString(copy));
    }

    // ================= SEARCH =================
    private static void handleSearch(Scanner scanner, int[] arr, ArrayOperations ops) {
        System.out.println("\n=== Linear Search ===");
        System.out.print("Enter element to search: ");

        if (!scanner.hasNextInt()) {
            System.out.println("Invalid input.");
            scanner.next();
            return;
        }

        int target = scanner.nextInt();
        int index = ops.linearSearch(arr, target);

        if (index != -1) {
            System.out.println("Element found at index: " + index);
        } else {
            System.out.println("Element not found.");
        }
    }
}
