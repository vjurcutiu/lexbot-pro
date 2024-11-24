from flask import Blueprint, jsonify
import os
from datetime import datetime
from database.models import db, File

filecheck_bp = Blueprint('filecheck', __name__)

# Path to the folder you want to monitor
folder_to_monitor = "c:/test"

def check_folder():
    """Check for new or updated files in the folder and update the database."""
    try:
        current_files = set(os.listdir(folder_to_monitor))  # Get all files in the folder
        file_paths = {file: os.path.join(folder_to_monitor, file) for file in current_files}

        new_files = []
        processed_files = []

        for file_name, full_path in file_paths.items():
            # Check if the file is already in the database
            file_record = File.query.filter_by(name=file_name).first()
            if file_record is None:
                # Add new file record
                new_file = File(
                    name=file_name,
                    path=full_path.replace("\\", "/"),
                    status="new",
                    created_at=datetime.utcnow(),
                    processed_at=None
                )
                db.session.add(new_file)
                new_files.append(file_name)

        # Commit changes to the database
        db.session.commit()

        return {
            "new_files": new_files,
            "processed_files": processed_files,
            "status": "success"
        }
    except Exception as e:
        db.session.rollback()  # Rollback changes if there's an error
        return {"error": str(e), "status": "failed"}

@filecheck_bp.route('/', methods=['POST'])
def filecheck():
    """Trigger a folder check and return results."""
    result = check_folder()
    return jsonify(result)
