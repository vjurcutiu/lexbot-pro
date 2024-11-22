import requests

# Define the URL of the Flask app
url = "http://127.0.0.1:5000/filecheck"

try:
    # Send a POST request to the /filecheck route
    response = requests.post(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the server's response
        print("Response from /filecheck:")
        print(response.json())
    else:
        # Print an error message if the request failed
        print(f"Error: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    # Handle exceptions (e.g., connection errors)
    print("Request failed:", str(e))
