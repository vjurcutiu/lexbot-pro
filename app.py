from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from routes.filecheck import filecheck_bp
from routes.chat import chat_bp
from routes.processing import processing_bp

from database.database import close_db
from database.models import db

# Initialize Flask app
app = Flask(__name__)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'main.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress warnings
db.init_app(app)

# Register routes
app.register_blueprint(filecheck_bp, url_prefix='/filecheck')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(processing_bp, url_prefix='/processing')

@app.route('/')
def index():
    return {"message": "Welcome to the LexBot Backend"}

# CLI command to inistialize the database
@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()  # Creates all tables defined in models.py
        print("Initialized the database with SQLAlchemy.")

# Register teardown function
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
