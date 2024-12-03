import requests

# URL of the Flask app endpoint
EMBED_URL = "http://127.0.0.1:5000/processing/embed"

def test_embed_function():
    try:
        # Send POST request to the /embed endpoint
        response = requests.post(EMBED_URL)

        # Print the response status and data
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")

    except Exception as e:
        print(f"An error occurred while testing the /embed function: {e}")

if __name__ == "__main__":
    test_embed_function()
