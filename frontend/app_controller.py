from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QStackedWidget, QWidget
from PySide6.QtCore import Qt

from pages.chat_page import ChatPage

from widgets.title_bar import TitleBar

from utils.messaging_handler import MessagingHandler

import concurrent.futures
import requests


class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LexBot Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Executor for threading
        self.executor = concurrent.futures.ThreadPoolExecutor()

        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("MainWindow")
        self.setCentralWidget(central_widget)

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
        """Delegate the message handling to the MessagingHandler."""
        self.messaging_handler.send_data_to_backend(user_message)
