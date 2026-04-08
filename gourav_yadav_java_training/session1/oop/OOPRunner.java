package gourav_yadav_java_training.session1.oop;



import java.util.Scanner;


public class OOPRunner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        demonstrateStudent(scanner);
        demonstrateGraduateStudent(scanner);

        scanner.close();
    }

    // ================= STUDENT =================
    private static void demonstrateStudent(Scanner scanner) {
        System.out.println("\n=== Student Example ===");

        System.out.print("Enter name: ");
        String name = scanner.next();

        System.out.print("Enter roll number: ");
        int roll = scanner.nextInt();

        System.out.print("Enter marks: ");
        double marks = scanner.nextDouble();

        Student student = new Student(name, roll, marks);

        student.displayDetails();

        // Overloaded method
        student.displayDetails("Basic Student Info");
    }

    // ================= GRADUATE STUDENT =================
    private static void demonstrateGraduateStudent(Scanner scanner) {
        System.out.println("\n=== Graduate Student Example ===");

        System.out.print("Enter name: ");
        String name = scanner.next();

        System.out.print("Enter roll number: ");
        int roll = scanner.nextInt();

        System.out.print("Enter marks: ");
        double marks = scanner.nextDouble();

        System.out.print("Enter research topic: ");
        String topic = scanner.next();

        GraduateStudent gradStudent = new GraduateStudent(name, roll, marks, topic);

        gradStudent.displayDetails();
    }
}