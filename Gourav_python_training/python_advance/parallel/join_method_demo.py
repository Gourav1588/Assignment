# Q3 - Demonstrate the use of join() method in threading.

import threading
import time

# Constants
SLEEP_SECONDS = 2


def slow_task(task_name) -> None:
    """Simulate a slow task using time.sleep()."""
    print(f"{task_name} started.")
    time.sleep(SLEEP_SECONDS)
    print(f"{task_name} finished.")


def demonstrate_join_method() -> None:
    """Demonstrate the use of join() method in threading."""
    task_thread = threading.Thread(target=slow_task, args=("Task-1",))
    task_thread.start()

    print("Main program is waiting for the thread to finish (join)...")
    task_thread.join()  # main thread pauses here until task_thread completes
    print("Main program continues after the thread finished.")


if __name__ == "__main__":
    demonstrate_join_method()