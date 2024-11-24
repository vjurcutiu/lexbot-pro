import requests

EMBED_ROUTE_URL = "http://127.0.0.1:5000/processing/embed"

def test_embed_route():
    """Test the /embed route."""
    print("Testing the /embed route with filecheck integration...")

    try:
        response = requests.post(EMBED_ROUTE_URL)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while testing the /embed route: {e}")

if __name__ == "__main__":
    test_embed_route()
