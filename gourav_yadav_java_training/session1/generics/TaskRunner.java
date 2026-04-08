package gourav_yadav_java_training.session1.generics;

public class TaskRunner extends Thread {

    private String taskName;

    public TaskRunner(String taskName) {
        this.taskName = taskName;
    }

    @Override
    public void run() {
        System.out.println("Started  : " + taskName + " | Thread: " + Thread.currentThread().getName());
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            System.out.println("Task interrupted: " + taskName);
            Thread.currentThread().interrupt();
        }
        System.out.println("Completed: " + taskName + " | Thread: " + Thread.currentThread().getName());
    }
}