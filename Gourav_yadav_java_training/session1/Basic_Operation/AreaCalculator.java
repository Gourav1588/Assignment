package Gourav_yadav_java_training.session1.basic_operation;


public class AreaCalculator {
    private static final double PI = 3.14159; 

    public double calculateCircleArea(double radius) {
        return PI * radius * radius;
    }

    public double calculateRectangleArea(double length, double width) {
        return length * width;
    }

    public double calculateTriangleArea(double base, double height) {
        return 0.5 * base * height;
    }
}