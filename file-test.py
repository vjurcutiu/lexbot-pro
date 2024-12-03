from app import app, db, File  # Replace 'your_flask_app' with the actual name of your Flask app package/module

def test_get_all_files():
    with app.app_context():  # Ensure the app context is active
        files = File.query.all()  # Retrieve all File records
        if not files:
            print("No records found in the database.")
        for file in files:
            print(file)  # This uses the __repr__ method of the File model

if __name__ == "__main__":
    test_get_all_files()