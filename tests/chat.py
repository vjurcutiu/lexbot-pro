import requests

# Define the URL of the Flask server
url = "http://127.0.0.1:5000/chat"

# Define the message payload
payload = {
    "message": "Yo, you there?"
}

try:
    # Send the POST request with the JSON payload
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response from the server
        print("Server Response:", response.json())
    else:
        # Print an error message if the request failed
        print(f"Error: {response.status_code}, {response.text}")

except requests.exceptions.RequestException as e:
    # Handle exceptions (e.g., connection errors)
    print("Request failed:", str(e))