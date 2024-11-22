import requests

BASE_URL = "http://127.0.0.1:5000"  # Replace with your Flask server URL

# Sample document data
sample_documents = [
    {"id": "doc1", "text": "Paris is the capital of France."},
    {"id": "doc2", "text": "The Eiffel Tower is one of the most famous landmarks in Paris."},
    {"id": "doc3", "text": "France is known for its wine and cheese."},
]

# Sample query
sample_query = "What is the capital of France?"

# Test the /embed endpoint
def test_embed_endpoint():
    print("Testing /embed endpoint...")
    for doc in sample_documents:
        response = requests.post(f"{BASE_URL}/processing/embed", json=doc)
        if response.status_code == 201:
            print(f"Document {doc['id']} embedded successfully!")
        else:
            print(f"Failed to embed document {doc['id']}: {response.text}")

# Test the /query endpoint
def test_query_endpoint():
    print("\nTesting /query endpoint...")
    query_data = {"query": sample_query}
    response = requests.post(f"{BASE_URL}/processing/query", json=query_data)
    if response.status_code == 200:
        results = response.json()
        print("Query Results:")
        for result in results:
            print(f" - Document ID: {result['id']}, Score: {result['score']}")
    else:
        print(f"Failed to retrieve query results: {response.text}")

# Test the /generate endpoint
def test_generate_endpoint():
    print("\nTesting /generate endpoint...")
    query_data = {"query": sample_query}
    response = requests.post(f"{BASE_URL}/processing/generate", json=query_data)
    if response.status_code == 200:
        result = response.json()
        print("Generated Response:")
        print(result["response"])
    else:
        print(f"Failed to generate response: {response.text}")

if __name__ == "__main__":
    # Test the endpoints in sequence
    test_embed_endpoint()
    test_query_endpoint()
    test_generate_endpoint()
