package gourav_yadav_java_training.session1.collections;



import java.util.Arrays;


public class StringHandler {

    //  program to reverse a given string 
    public String reverseString(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();
    }

    // function to count the number of vowels in a string 
    public int countVowels(String str) {
        if (str == null) return 0;
        int count = 0;
        String lowerStr = str.toLowerCase();
        for (int i = 0; i < lowerStr.length(); i++) {
            char c = lowerStr.charAt(i);
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
                count++;
            }
        }
        return count;
    }
    //  program to check if two strings are anagram
    public boolean areAnagrams(String s1, String s2) {
        if (s1 == null || s2 == null) return false;
        
        // Remove whitespace and convert to lowercase for accurate comparison
        char[] array1 = s1.replaceAll("\\s", "").toLowerCase().toCharArray();
        char[] array2 = s2.replaceAll("\\s", "").toLowerCase().toCharArray();
        
        if (array1.length != array2.length) return false;
        
        Arrays.sort(array1);
        Arrays.sort(array2);
        
        return Arrays.equals(array1, array2);
    }
}
