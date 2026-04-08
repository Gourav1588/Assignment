package gourav_yadav_java_training.session1.oop;



/**
 * Demonstrates Inheritance + Method Overriding
 */
public class GraduateStudent extends Student {

    private String researchTopic;

    public GraduateStudent(String name, int rollNumber, double marks, String researchTopic) {
        super(name, rollNumber, marks);
        this.researchTopic = researchTopic;
    }

    public String getResearchTopic() {
        return researchTopic;
    }

    public void setResearchTopic(String researchTopic) {
        this.researchTopic = researchTopic;
    }

    // Runtime Polymorphism (Method Overriding)
    @Override
    public void displayDetails() {
        super.displayDetails();
        System.out.println("Research Topic: " + researchTopic);
    }
}
