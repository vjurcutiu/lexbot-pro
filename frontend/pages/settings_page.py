from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # Reference to AppController

        layout = QVBoxLayout(self)

        # Settings area
        self.settings_label = QLabel("Settings Screen")
        self.settings_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.settings_label)

        # Button to navigate back to chat
        self.back_button = QPushButton("Back to Chat")
        self.back_button.clicked.connect(self.controller.show_chat_page)
        layout.addWidget(self.back_button)
