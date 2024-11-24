import sys
import requests  # To send HTTP requests to Flask
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from interface import Ui_MainWindow  # Import the generated UI file

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the window flags to create a borderless window
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # Connect button click to a method
        self.ui.pushButton.clicked.connect(self.send_data_to_backend)

    def send_data_to_backend(self):
        # Collect data from the GUI
        user_input = self.ui.textEdit.toPlainText()

        # Prepare the data for the Flask backend
        payload = {"message": user_input}

        try:
            # Send the data to Flask
            response = requests.post("http://127.0.0.1:5000/chat", json=payload)
            if response.status_code == 200:
                result = response.json()
                self.ui.textBrowser.setText(f"Backend Response: {result}")
            else:
                self.ui.textBrowser.setText(f"Error: {response}")
        except Exception as e:
            self.ui.textBrowser.setText(f"Connection error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
