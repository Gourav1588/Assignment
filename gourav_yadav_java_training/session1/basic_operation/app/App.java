package gourav_yadav_java_training.session1.basic_operation.app;

import java.util.Scanner;
import gourav_yadav_java_training.session1.basic_operation.service.*;

public class App {

    private Scanner scanner = new Scanner(System.in);

    private AreaService areaService = new AreaService();
    private MathService mathService = new MathService();
    private PatternService patternService = new PatternService();
    private OperatorService operatorService = new OperatorService();
    private TemperatureService temperatureService = new TemperatureService();
    private NumberService numberService = new NumberService();
    private LoopService loopService = new LoopService();
    private CompareService compareService = new CompareService();

    public void start() {

        while (true) {

            System.out.println("\n===== MAIN MENU =====");
            System.out.println("1. Area Calculator");
            System.out.println("2. Math Operations");
            System.out.println("3. Pattern Printing");
            System.out.println("4. Operator Demo");
            System.out.println("5. Temperature Converter");
            System.out.println("6. Number Operations");
            System.out.println("7. Loop Operations");
            System.out.println("8. Comparison Demo");
            System.out.println("9. Exit");
            System.out.print("Enter your choice: ");

            if (!scanner.hasNextInt()) {
                System.out.println("Invalid input.");
                scanner.next();
                continue;
            }

            int choice = scanner.nextInt();

            switch (choice) {

                case 1:
                    areaService.process(scanner);
                    break;

                case 2:
                    mathService.process(scanner);
                    break;

                case 3:
                    patternService.process(scanner);
                    break;

                case 4:
                    operatorService.process(scanner);
                    break;

                case 5:
                    temperatureService.process(scanner);
                    break;

                case 6:
                    numberService.process(scanner);
                    break;

                case 7:
                    loopService.process(scanner);
                    break;

                case 8:
                    compareService.process();
                    break;

                case 9:
                    System.out.println("Exiting program...");
                    scanner.close();
                    return;

                default:
                    System.out.println("Invalid choice.");
            }
        }
    }
}