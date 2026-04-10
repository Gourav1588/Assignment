package gourav_yadav_java_training.session1.generics;


import java.io.*;

public class FileManager {

    public void performFileIO(String fileName) {

        // Writing data to file
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(fileName))) {
            bw.write("Java Assignment 2026 - File I/O Task\n");
            bw.write("Written successfully using BufferedWriter.");
            System.out.println("Data written to file: " + fileName);
        } catch (IOException e) {
            System.out.println("Write Error: " + e.getMessage());
        }

        // Reading data from file
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            System.out.println("\n--- Reading File Content ---");
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.out.println("Read Error: " + e.getMessage());
        }
    }
}
