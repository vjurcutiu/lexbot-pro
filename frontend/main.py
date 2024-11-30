import sys
import os
import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QTextEdit, QPlainTextEdit, QMenuBar, QMenu, QFileDialog, QDialog, QLabel, QLineEdit
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer, Qt
from datetime import datetime

class SettingsDialog(QDialog):
    """Dialog for selecting a folder and API keys."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 500, 200)

        # Layout for the dialog
        layout = QVBoxLayout()

        # Folder selection label and input
        self.folder_label = QLabel("Select Folder:")
        self.folder_input = QLineEdit(self)
        self.folder_input.setPlaceholderText("No folder selected...")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_folder)

        # Horizontal layout for folder input and browse button
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_button)

        # OpenAI API Key input
        self.openai_label = QLabel("OpenAI API Key:")
        self.openai_input = QLineEdit(self)
        self.openai_input.setPlaceholderText("Enter OpenAI API Key...")
        self.openai_confirm_button = QPushButton("Confirm")
        self.openai_confirm_button.clicked.connect(self.confirm_openai_api)

        # Horizontal layout for OpenAI API input and confirm button
        openai_layout = QHBoxLayout()
        openai_layout.addWidget(self.openai_input)
        openai_layout.addWidget(self.openai_confirm_button)

        # Pinecone API Key input
        self.pinecone_label = QLabel("Pinecone API Key:")
        self.pinecone_input = QLineEdit(self)
        self.pinecone_input.setPlaceholderText("Enter Pinecone API Key...")
        self.pinecone_confirm_button = QPushButton("Confirm")
        self.pinecone_confirm_button.clicked.connect(self.confirm_pinecone_api)

        # Horizontal layout for Pinecone API input and confirm button
        pinecone_layout = QHBoxLayout()
        pinecone_layout.addWidget(self.pinecone_input)
        pinecone_layout.addWidget(self.pinecone_confirm_button)

        # OK and Cancel buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.send_folder_to_backend)  # Send folder to backend
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # Close the dialog with reject

        # Horizontal layout for OK/Cancel buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Add widgets to the main layout
        layout.addWidget(self.folder_label)
        layout.addLayout(folder_layout)
        layout.addWidget(self.openai_label)
        layout.addLayout(openai_layout)
        layout.addWidget(self.pinecone_label)
        layout.addLayout(pinecone_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def select_folder(self):
        """Open a dialog to select a folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def confirm_openai_api(self):
        """Transform OpenAI API input into dots."""
        text = self.openai_input.text()
        if text:
            self.openai_input.setText("•" * len(text))

    def confirm_pinecone_api(self):
        """Transform Pinecone API input into dots."""
        text = self.pinecone_input.text()
        if text:
            self.pinecone_input.setText("•" * len(text))

    def send_folder_to_backend(self):
        """Send the selected folder path to the backend."""
        folder_path = self.folder_input.text().strip()
        if not folder_path:
            self.parent().chat_display.append("<div style='color:orange;'>No folder selected.</div>")
            return

        # Prepare the payload
        payload = {"folder_path": folder_path}

        try:
            # Send the folder path to the Flask backend
            response = requests.post("http://127.0.0.1:5000/filecheck", json=payload)

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    new_files = result.get("new_files", [])
                    self.parent().chat_display.append(
                        f"<div style='color:green;'>New Files: {', '.join(new_files)}</div>"
                    )
                else:
                    error_message = result.get("error", "Unknown error")
                    self.parent().chat_display.append(
                        f"<div style='color:red;'>Error: {error_message}</div>"
                    )
            else:
                self.parent().chat_display.append(
                    f"<div style='color:red;'>Backend responded with status {response.status_code}</div>"
                )
        except Exception as e:
            self.parent().chat_display.append(
                f"<div style='color:red;'>Connection error: {str(e)}</div>"
            )

        self.accept()  # Close the dialog after sending



class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LexBot Pro")
        self.setGeometry(100, 100, 800, 600)

        # Add File Menu
        self.create_menu()

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QHBoxLayout(central_widget)

        # Left Widget: Previous Chats
        self.chat_list = QListWidget()
        self.chat_list.setFixedWidth(200)
        self.chat_list.addItem("Conversatii recente")
        main_layout.addWidget(self.chat_list)

        # Right Layout: Chat Display and Input
        right_layout = QVBoxLayout()

        # Central Chat Widget
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        right_layout.addWidget(self.chat_display)

        # Bottom Input Layout
        input_layout = QHBoxLayout()
        self.input_field = ChatInputField(self)
        self.input_field.setFixedHeight(50)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(50)
        self.send_button.clicked.connect(self.send_data_to_backend)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        right_layout.addLayout(input_layout)

        main_layout.addLayout(right_layout)

        # Load external styles
        self.load_styles()

    def create_menu(self):
        """Create a File menu in the toolbar with Settings and Exit options."""
        menu_bar = self.menuBar()  # Create the menu bar
        file_menu = menu_bar.addMenu("File")  # Add File menu to the menu bar

        # Add Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)  # Connect to a slot
        file_menu.addAction(settings_action)

        # Add Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close_application)  # Connect to close the app
        file_menu.addAction(exit_action)

    def open_settings(self):
        """Open the Settings dialog."""
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec() == QDialog.Accepted:
            selected_folder = settings_dialog.folder_input.text()
            if selected_folder:
                self.chat_display.append(f"<div style='color:purple;'>Selected Folder: {selected_folder}</div>")
            else:
                self.chat_display.append("<div style='color:orange;'>No folder selected.</div>")

    def close_application(self):
        """Close the application."""
        self.close()

    def load_styles(self):
        """Loads QSS styles from the styles.qss file."""
        style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def send_data_to_backend(self):
        """Send data to the backend and handle responses."""
        user_input = self.input_field.toPlainText().strip()
        if not user_input:
            self.append_to_chatbox("You: (Empty message)", "warning")
            return

        # Append the user's full message to the chat window
        self.append_to_chatbox(f"You: {user_input}", "user")

        # Prepare the data for the Flask backend
        payload = {"message": user_input}

        # Clear the input field
        self.input_field.clear()

        try:
            # Send the data to Flask
            response = requests.post("http://127.0.0.1:5000/chat", json=payload)
            if response.status_code == 200:
                result = response.json()
                backend_response = result.get("response", "(No response received)")

                # Delay the bot's response by half a second
                QTimer.singleShot(500, lambda: self.append_to_chatbox(f"LexBot: {backend_response}", "bot"))
            else:
                self.append_to_chatbox(f"Error: Backend responded with status {response.status_code}", "error")
        except Exception as e:
            self.append_to_chatbox(f"Connection error: {e}", "error")

    def append_to_chatbox(self, message, message_type="info"):
        """Append a message to the chatbox (QTextEdit) with a timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        styled_message = f"<b>[{timestamp}]</b> {message.replace('\n', '<br>')}"

        # Style messages based on type
        if message_type == "user":
            styled_message = f"<div style='color:blue; margin-bottom:10px;'>{styled_message}</div>"
        elif message_type == "bot":
            styled_message = f"<div style='color:green; margin-bottom:10px;'>{styled_message}</div>"
        elif message_type == "error":
            styled_message = f"<div style='color:red; margin-bottom:10px;'>{styled_message}</div>"
        elif message_type == "warning":
            styled_message = f"<div style='color:orange; margin-bottom:10px;'>{styled_message}</div>"

        self.chat_display.append(styled_message)


class ChatInputField(QPlainTextEdit):
    """Custom input field to handle Enter and Shift+Enter."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() == Qt.ShiftModifier:
                self.insertPlainText("\n")  # Add a new line in the input field
            else:
                self.parent.send_data_to_backend()  # Send the full message
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
