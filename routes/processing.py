from flask import Blueprint, request, jsonify
import os
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from database.models import db, File
from datetime import datetime
import requests
from PyPDF2 import PdfReader
from docx import Document
import chardet
from config import client, assistant

processing_bp = Blueprint('processing', __name__)

FILECHECK_ROUTE_URL = "http://127.0.0.1:5000/filecheck"

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
def generate_and_store_embeddings():
    try:
        #Trigger the filecheck route
        filecheck_response = requests.post(FILECHECK_ROUTE_URL)
        if filecheck_response.status_code != 200:
            return jsonify({"error": "Filecheck failed", "details": filecheck_response.json()}), 500


        # Query the database for files with status 'new'
        new_files = File.query.filter_by(status="new").all()
        if not new_files:
            return jsonify({"message": "No new files to process."}), 200
        
        processed_files = []

        for file_record in new_files:
            try:
                # Determine the file path and type
                file_path = file_record.path
                file_extension = os.path.splitext(file_path)[-1].lower()

                # Initialize variable to hold text content
                text = ""

                # Extract text based on file type
                if file_extension == ".pdf":
                    reader = PdfReader(file_path)
                    text = " ".join([page.extract_text() for page in reader.pages])
                    print(text)

                elif file_extension == ".docx":
                    doc = Document(file_path)
                    text = " ".join([paragraph.text for paragraph in doc.paragraphs])
                    print(text)

                elif file_extension in [".txt", ".csv"]:
                    with open(file_path, "rb") as file:
                        # Detect encoding
                        raw_data = file.read()
                        result = chardet.detect(raw_data)
                        encoding = result["encoding"]
                        text = raw_data.decode(encoding)
                        print(text)                    

                else:
                    print(f"Unsupported file type for: {file_path}")
                    continue

                if not text.strip():
                    print(f"No text extracted from file: {file_path}")
                    continue  # Skip this file if no text content is available

                # Generate embedding using OpenAI
                response = client.embeddings.create(
                    input=text,
                    model="text-embedding-3-large"
                )
                print(response)
                embedding = response.data[0].embedding

                # Store embedding in Pinecone
                index.upsert([(str(file_record.id), embedding)])

                # Update the file record in the database
                file_record.status = "embedded"
                file_record.processed_at = datetime.utcnow()
                db.session.commit()

                processed_files.append(file_record.id)

            except Exception as e:
                print(f"Error processing file {file_record.path}: {e}")
                db.session.rollback()  # Rollback database changes if there's an error        
        
        if not processed_files:
            return jsonify({"message": "No files were successfully processed."}), 500

        return jsonify({"message": f"Successfully processed files: {processed_files}"}), 201


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
    if not client or not assistant:
        return jsonify({"error": "Assistant is not initialized. Please contact the administrator."}), 500

    data = request.json
    query = data.get("query")  # User query
    

    try:
        # Create a thread and attach the file to the message
        thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": query,
            }
        ]
        )
        
        # The thread now has a vector store with that file in its tool resources.
        print(thread.tool_resources.file_search)

        # Use the create and poll SDK helper to create a run and poll the status of
        # the run until it's in a terminal state.

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")
        
        print(message_content.value)
        print("\n".join(citations))

        return jsonify({
            "response": message_content.value,
            "citations": citations
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
