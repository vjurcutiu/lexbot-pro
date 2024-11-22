from flask import Blueprint, request, jsonify
import os

filecheck_bp = Blueprint('filecheck', __name__)

# Path to the folder you want to monitor
folder_to_monitor = "c:/test"

# A set to store filenames we've already seen
seen_files = set()

def check_folder():
    """Check for new files in the folder and return them."""
    global seen_files
    try:
        current_files = set(os.listdir(folder_to_monitor))
        new_files = current_files - seen_files
        if new_files:
            seen_files.update(new_files)
        return {"new_files": list(new_files), "status": "success"}
        # Return all files
    except Exception as e:
        return {"error": str(e), "status": "failed"}

@filecheck_bp.route('/', methods=['POST'])
def filecheck():
    """Trigger a folder check and return results."""
    result = check_folder()
    return jsonify(result)
