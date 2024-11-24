from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

from routes.filecheck import filecheck_bp
from routes.chat import chat_bp
from routes.processing import processing_bp

from database.database import close_db
from database.models import db, File

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

@app.route('/view-entries', methods=['GET'])
def view_entries():
    """View all entries in the File table."""
    files = File.query.all()
    return jsonify([
        {
            "id": file.id,
            "name": file.name,
            "path": file.path,
            "status": file.status,
            "created_at": file.created_at,
            "processed_at": file.processed_at
        }
        for file in files
    ])

# CLI command to inistialize the database
@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()  # Creates all tables defined in models.py
        print("Initialized the database with SQLAlchemy.")

@app.cli.command("clear-table")
def clear_table():
    """Remove all entries from the File table."""
    with app.app_context():
        try:
            db.session.query(File).delete()  # Deletes all rows in the File table
            db.session.commit()  # Commit the changes
            print("All entries removed from the File table.")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error clearing table: {e}")

# Register teardown function
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
