from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class ChatBubble(QWidget):
    def __init__(self, message, citations=None, is_user=False, parent_width=800):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)

        # Align the bubble
        if is_user:
            self.layout.setAlignment(Qt.AlignRight)
            bubble_color = "#2F2F2F"  # User message color
            text_color = "white"
        else:
            self.layout.setAlignment(Qt.AlignLeft)
            bubble_color = "#F1F1F1"  # Bot message color
            text_color = "black"

        # Calculate the fixed width (60% of the parent width)
        self.bubble_width = int(parent_width * 0.6)

        # Bubble label
        self.bubble_label = QLabel(message)  # Save as an instance attribute
        self.bubble_label.setStyleSheet(f"""
            background-color: {bubble_color};
            color: {text_color};
            border-radius: 10px;
            padding: 10px;
        """)
        self.bubble_label.setWordWrap(True)
        self.bubble_label.setFixedWidth(self.bubble_width)  # Set fixed width
        self.layout.addWidget(self.bubble_label)

        # Citations (optional)
        if citations:                    
            citations_text = "\n".join(f"[{i+1}] {citation}" for i, citation in enumerate(citations))
            self.citations_label = QLabel(citations_text)
            self.citations_label.setStyleSheet("color: gray; font-size: 12px; margin-top: 5px;")
            self.citations_label.setWordWrap(True)
            self.layout.addWidget(self.citations_label)

    def set_message(self, message, citations):
        """Update the message and citations."""        

        if citations:
            citations_text = "\n".join(f"[{i+1}] {citation}" for i, citation in enumerate(citations))
            package = message + citations_text
            self.bubble_label.setText(package)
        else:
            self.bubble_label.setText(message)


