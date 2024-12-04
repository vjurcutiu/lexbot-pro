import os

def get_stylesheet():
    """Load and return the application stylesheet from styles.qss."""
    style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            return f.read()
    return ""  # Return an empty string if the file does not exist