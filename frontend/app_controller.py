from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QStackedWidget, QWidget, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from pages.chat_page import ChatPage

from widgets.title_bar import TitleBar

from utils.messaging_handler import MessagingHandler

import concurrent.futures

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LexBot Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Frameless for custom styling
        self.setAttribute(Qt.WA_TranslucentBackground)  # Allow translucent background

        # Executor for threading
        self.executor = concurrent.futures.ThreadPoolExecutor()

        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("MainWindow")
        self.setCentralWidget(central_widget)

        # Apply shadow effect to the central widget
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(30)  # Softness of the shadow
        shadow_effect.setColor(QColor(0, 0, 0, 75))
        shadow_effect.setOffset(2, 10)  # Centered shadow
        central_widget.setGraphicsEffect(shadow_effect)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Add title bar
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Stacked widget for screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Add chat page
        self.chat_page = ChatPage(self)
        self.stacked_widget.addWidget(self.chat_page)

        # Show chat page by default
        self.stacked_widget.setCurrentWidget(self.chat_page)

        # Initialize MessagingHandler
        self.messaging_handler = MessagingHandler(
            backend_url="http://127.0.0.1:5000/processing/generate",
            on_message=self.chat_page.add_message
        )

    def send_data_to_backend(self, user_message):
        """Send the user's message to the backend."""
        self.messaging_handler.send_data_to_backend(user_message)
