from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QPlainTextEdit, QScrollArea, QLabel, QFrame
)
from PySide6.QtCore import Qt, QPoint
from datetime import datetime
import requests
import sys
import os


class ChatBubble(QWidget):
    def __init__(self, message, is_user=False, parent_width=800):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Align the bubble based on user or bot
        if is_user:
            layout.setAlignment(Qt.AlignRight)
            bubble_color = "#0078D7"  # User message color
            text_color = "white"
        else:
            layout.setAlignment(Qt.AlignLeft)
            bubble_color = "#E5E5EA"  # Bot message color
            text_color = "black"

        # Calculate the fixed width (40% of the parent width)
        bubble_width = int(parent_width * 0.4)

        # Bubble label with dynamic vertical resizing
        bubble_label = QLabel(message)
        bubble_label.setStyleSheet(f"""
            background-color: {bubble_color};
            color: {text_color};
            border-radius: 10px;
            padding: 10px;
        """)
        bubble_label.setWordWrap(True)  # Enable text wrapping
        bubble_label.setFixedWidth(bubble_width)  # Set fixed width

        # Align text within the bubble
        bubble_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Add label to layout
        layout.addWidget(bubble_label)



class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LexBot Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.dragging = False
        self.offset = QPoint()

        central_widget = QWidget()
        central_widget.setObjectName("MainWindow")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 0, 5, 5)  # No margins for rounded corners

        self.create_title_bar(main_layout)
        self.create_main_content(main_layout)
        self.load_styles()

    def create_title_bar(self, main_layout):
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("LexBot Pro")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.minimize_button = QPushButton("-")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFixedWidth(40)

        self.maximize_button = QPushButton("⬜")
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.maximize_button.setFixedWidth(40)

        self.close_button = QPushButton("×")
        self.close_button.clicked.connect(self.close_application)
        self.close_button.setFixedWidth(40)

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.maximize_button)
        title_layout.addWidget(self.close_button)

        main_layout.addWidget(title_bar)

        title_bar.mousePressEvent = self.start_drag
        title_bar.mouseMoveEvent = self.perform_drag
        title_bar.mouseReleaseEvent = self.stop_drag

    def create_main_content(self, main_layout):
        # Scrollable chat display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        # Chat bubbles container
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.messages_widget)
        main_layout.addWidget(self.scroll_area)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = ChatInputField(self)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_data_to_backend)
        input_layout.addWidget(self.input_field)
        main_layout.addLayout(input_layout)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def close_application(self):
        self.close()

    def load_styles(self):
        style_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())

    def start_drag(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()

    def perform_drag(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def stop_drag(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def send_data_to_backend(self):
        user_input = self.input_field.toPlainText().strip()
        if not user_input:
            self.add_message("You: (Empty message)", "warning")
            return

        self.add_message(f"You: {user_input}", is_user=True)

        payload = {"query": user_input}
        self.input_field.clear()

        try:
            response = requests.post("http://127.0.0.1:5000/processing/generate", json=payload)
            if response.status_code == 200:
                result = response.json()
                bot_message = result.get("response", "(No response received)")
                self.add_message(bot_message, is_user=False)
            else:
                self.add_message(f"Error: Backend responded with status {response.status_code}", is_user=False)
        except Exception as e:
            self.add_message(f"Connection error: {e}", is_user=False)

    def add_message(self, message, is_user):
        bubble = ChatBubble(message, is_user)
        self.messages_layout.addWidget(bubble)
        # Auto-scroll to the bottom
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


class ChatInputField(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(75)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() == Qt.ShiftModifier:
                self.insertPlainText("\n")
            else:
                self.parent.send_data_to_backend()
                self.clear()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())
