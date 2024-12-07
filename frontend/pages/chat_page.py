from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QPushButton
from PySide6.QtCore import Qt
from widgets.chat_input_field import ChatInputField
from widgets.chat_bubble import ChatBubble  # Assuming ChatBubble is also modularized


class ChatPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller  # Reference to AppController
        self.executor = controller.executor

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 5)

        # Scrollable chat display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        # Chat bubbles container
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.messages_widget)
        layout.addWidget(self.scroll_area)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = ChatInputField()
        self.input_field.setObjectName('InputField')
        self.input_field.messageSubmitted.connect(self.handle_message_submitted)  # Connect signal

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send_button_clicked)
        input_layout.addWidget(self.input_field)

        layout.addLayout(input_layout)

        # Add an initial message
        self.add_message("Welcome to LexBot Pro! Ask me anything.", is_user=False)

    def add_message(self, message, is_user, is_loading=False, citations=None):
        bubble = ChatBubble("Typing..." if is_loading else message, citations=citations, is_user=is_user)
        self.messages_layout.addWidget(bubble)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        return bubble


    def handle_message_submitted(self, message):
        """Handle message submission from the input field."""
        self.controller.send_data_to_backend(message)

    def handle_send_button_clicked(self):
        """Handle the send button click."""
        message = self.input_field.toPlainText().strip()
        if message:
            self.controller.send_data_to_backend(message)
            self.input_field.clear()
