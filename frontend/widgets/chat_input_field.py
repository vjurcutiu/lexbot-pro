from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt


class ChatInputField(QPlainTextEdit):
    messageSubmitted = Signal(str)  # Signal emitted when a message is submitted

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(75)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() == Qt.ShiftModifier:
                self.insertPlainText("\n")  # Add a new line for Shift+Enter
            else:
                # Emit the submitted message as a signal
                message = self.toPlainText().strip()
                if message:  # Avoid emitting empty messages
                    self.messageSubmitted.emit(message)
                self.clear()  # Clear the input field
        else:
            super().keyPressEvent(event)
