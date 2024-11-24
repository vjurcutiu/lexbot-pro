import sys
import requests  # To send HTTP requests to Flask
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
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
        user_input = self.ui.textEdit.toPlainText().strip()
        if not user_input:
            self.append_to_chatbox("You: (Empty message)", "warning")
            return

        # Append the user's message to the chat window with a timestamp
        self.append_to_chatbox(f"You: {user_input}", "user")

        # Prepare the data for the Flask backend
        payload = {"message": user_input}

        try:
            # Send the data to Flask
            response = requests.post("http://127.0.0.1:5000/chat", json=payload)
            if response.status_code == 200:
                result = response.json()
                backend_response = result.get("response", "(No response received)")

                # Delay the bot's response by half a second
                QTimer.singleShot(500, lambda: self.append_to_chatbox(f"Bot: {backend_response}", "bot"))
            else:
                self.append_to_chatbox(f"Error: Backend responded with status {response.status_code}", "error")
        except Exception as e:
            self.append_to_chatbox(f"Connection error: {e}", "error")

    def append_to_chatbox(self, message, message_type="info"):
        """Append a message to the chatbox (QTextBrowser) with a timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        styled_message = f"<b>[{timestamp}]</b> {message}"

        # Style messages based on type
        if message_type == "user":
            styled_message = f"<span style='color:blue;'>{styled_message}</span>"
        elif message_type == "bot":
            styled_message = f"<span style='color:green;'>{styled_message}</span>"
        elif message_type == "error":
            styled_message = f"<span style='color:red;'>{styled_message}</span>"
        elif message_type == "warning":
            styled_message = f"<span style='color:orange;'>{styled_message}</span>"

        # Append the styled message to the chatbox
        current_text = self.ui.textBrowser.toHtml()  # Get the current HTML content
        new_text = f"{current_text}<br>{styled_message}"  # Append the new message
        self.ui.textBrowser.setHtml(new_text)  # Set the updated content
        self.ui.textBrowser.verticalScrollBar().setValue(self.ui.textBrowser.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
