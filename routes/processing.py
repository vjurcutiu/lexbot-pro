from flask import Blueprint, request, jsonify
import os
from openai import OpenAI
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # Pinecone API key
    environment=os.getenv("PINECONE_ENV")  # Pinecone environment (e.g., "us-west1-gcp")
)

# Define the Pinecone index name
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")