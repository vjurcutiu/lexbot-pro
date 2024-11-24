from flask import Blueprint, request, jsonify
import os
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

processing_bp = Blueprint('processing', __name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# Define the Pinecone index name
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Retrieve the list of existing indexes
indexes = pc.list_indexes()

# Extract and print the names of the indexes
index_names = [index['name'] for index in indexes]


# Ensure the index exists
if INDEX_NAME not in index_names:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # OpenAI's embedding dimension
        metric="cosine",
        spec= ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )
index = pc.Index(INDEX_NAME)

@processing_bp.route('/embed', methods=['POST'])
def generate_and_store_embedding():
    data = request.json
    document_id = data.get("id")  # Unique ID for the document
    text = data.get("text")  # Document text

    try:
        # Generate embedding using OpenAI
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        print(response)
        embedding = response.data[0].embedding
        
        # Store embedding in Pinecone
        index.upsert([(document_id, embedding)])
        return jsonify({"message": f"Document {document_id} stored successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@processing_bp.route('/query', methods=['POST'])
def query_retrieval():
    data = request.json
    query = data.get("query")  # User query

    try:
        # Generate query embedding using OpenAI
        response = client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = response.data[0].embedding

        # Perform a search in Pinecone
        search_results = index.query(
            vector=query_embedding,
            top_k=5,  # Number of results to retrieve
            include_metadata=True  # Include metadata if stored
        )

        # Format the results
        results = [
            {"id": match["id"], "score": match["score"]}
            for match in search_results["matches"]
        ]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@processing_bp.route('/generate', methods=['POST'])
def generate_response():
    data = request.json
    query = data.get("query")  # User query

    try:
        # Generate query embedding
        response = client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = response.data[0].embedding

        # Retrieve top documents from Pinecone
        search_results = index.query(
            vector=query_embedding,
            top_k=3,  # Adjust for number of documents to retrieve
            include_metadata=True
        )

        # Concatenate retrieved documents        
        context = [item for match in search_results["matches"] for item in match['values']]

        # Query OpenAI with context
        openai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {query}"
                },
                {"role": "system", "content": "Answer:"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        generated_answer = openai_response.choices[0].message.content

        return jsonify({"response": generated_answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
