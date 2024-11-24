import os
import requests
from time import sleep

# URL of your Flask app's filecheck endpoint
FILECHECK_URL = "http://127.0.0.1:5000/filecheck"

# Path to the folder being monitored (match it with your Flask app configuration)
FOLDER_TO_MONITOR = "c:/test"

# Ensure the monitored folder exists
os.makedirs(FOLDER_TO_MONITOR, exist_ok=True)

def create_test_files(file_names):
    """Create test files in the monitored folder."""
    for file_name in file_names:
        file_path = os.path.join(FOLDER_TO_MONITOR, file_name)
        with open(file_path, 'w') as f:
            f.write(f"This is a test file: {file_name}\n")
    print(f"Created test files: {file_names}")

def test_filecheck():
    """Send a POST request to the filecheck endpoint and print the response."""
    try:
        response = requests.post(FILECHECK_URL)
        print("Response from filecheck endpoint:")
        print(response.json())
    except Exception as e:
        print(f"Error during request: {e}")

def main():
    """Main function to simulate file addition and test filecheck."""
    print("Starting test...")

    # Step 1: Simulate adding new files
    new_files = ["test_file1.txt", "test_file2.txt"]
    create_test_files(new_files)

    # Step 2: Allow some time for changes (optional)
    sleep(2)

    # Step 3: Trigger the filecheck endpoint
    print("Triggering filecheck endpoint...")
    test_filecheck()

    # Step 4: Simulate adding more files
    additional_files = ["test_file3.txt", "test_file4.txt"]
    create_test_files(additional_files)

    # Step 5: Trigger the filecheck endpoint again
    print("Triggering filecheck endpoint after adding more files...")
    test_filecheck()

    # Step 6: Check processed files by triggering the endpoint again without adding new files
    print("Triggering filecheck endpoint with no new files...")
    test_filecheck()

if __name__ == "__main__":
    main()
