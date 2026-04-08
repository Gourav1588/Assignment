package Gourav_yadav_java_training.session1.basic_operation;

public class TempConverter {
    public double toFahrenheit(double celsius) {
        return (celsius * 9 / 5) + 32;
    }

    public double toCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5 / 9;
    }
}
