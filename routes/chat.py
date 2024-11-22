from flask import Blueprint, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv



chat_bp = Blueprint('chat', __name__)

# Load environment variables
load_dotenv()

# Set your OpenAI API key
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

@chat_bp.route('/', methods=['POST'])
def chat():
    # Get the string from the user
    user_input = request.json.get('message', '')

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Send the input to OpenAI Chat Completions API
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ])

        # Extract and print the response
        ai_response = response.choices[0].message.content
        print("AI Response:", ai_response)

        # Return the response to the user
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
