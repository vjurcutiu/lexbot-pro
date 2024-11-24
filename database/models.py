from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    path = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.String(50), default="new")  # Status: new, processed, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<File {self.name} ({self.status})>"