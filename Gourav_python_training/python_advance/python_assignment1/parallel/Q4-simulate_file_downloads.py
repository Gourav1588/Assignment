# Q4 - Create multiple threads to simulate file downloading using time.sleep().

import threading
import time

# Constants
DOWNLOAD_FILE_NAMES = ["file1.zip", "file2.zip", "file3.zip"]
DOWNLOAD_SIMULATION_SECONDS = 2


def simulate_file_download(file_name) -> None:
    """Simulate downloading a single file using time.sleep()."""
    print(f"Starting download: {file_name}")
    time.sleep(DOWNLOAD_SIMULATION_SECONDS)  # simulate network delay
    print(f"Finished download: {file_name}")


def simulate_multiple_file_downloads() -> None:
    """Create multiple threads to simulate file downloading using time.sleep()."""
    download_threads = []

    for file_name in DOWNLOAD_FILE_NAMES:
        thread = threading.Thread(target=simulate_file_download, args=(file_name,))
        download_threads.append(thread)
        thread.start()

    for thread in download_threads:
        thread.join()

    print("All downloads completed.")


if __name__ == "__main__":
    simulate_multiple_file_downloads()