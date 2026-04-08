package gourav_yadav_java_training.session1.collections;



import java.util.Scanner;

public class StringHandlerRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StringHandler handler = new StringHandler();

        handleReverseString(scanner, handler);
        handleVowelCount(scanner, handler);
        handleAnagramCheck(scanner, handler);

        scanner.close();
    }

    // ================= REVERSE STRING =================
    private static void handleReverseString(Scanner scanner, StringHandler handler) {
        System.out.println("\n=== Reverse String ===");
        System.out.print("Enter a string: ");

        String input = scanner.nextLine();
        String reversed = handler.reverseString(input);

        System.out.println("Reversed String: " + reversed);
    }

    // ================= COUNT VOWELS =================
    private static void handleVowelCount(Scanner scanner, StringHandler handler) {
        System.out.println("\n=== Count Vowels ===");
        System.out.print("Enter a string: ");

        String input = scanner.nextLine();
        int count = handler.countVowels(input);

        System.out.println("Number of vowels: " + count);
    }

    // ================= ANAGRAM CHECK =================
    private static void handleAnagramCheck(Scanner scanner, StringHandler handler) {
        System.out.println("\n=== Anagram Check ===");

        System.out.print("Enter first string: ");
        String s1 = scanner.nextLine();

        System.out.print("Enter second string: ");
        String s2 = scanner.nextLine();

        boolean result = handler.areAnagrams(s1, s2);

        if (result) {
            System.out.println("The strings are anagrams.");
        } else {
            System.out.println("The strings are NOT anagrams.");
        }
    }
}