from flask import Flask

from routes.filecheck import filecheck_bp
from routes.chat import chat_bp

import os

# Initialize Flask app
app = Flask(__name__)

#Register routes
app.register_blueprint(filecheck_bp, url_prefix='/filecheck')
app.register_blueprint(chat_bp, url_prefix='/chat')

@app.route('/')
def index():
    return {"message": "Welcome to the LexBot Backend"}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
