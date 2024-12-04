from PySide6.QtWidgets import QApplication
from app_controller import AppController
from utils.styles import get_stylesheet
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppController()

    # Apply the stylesheet
    stylesheet = get_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window.show()
    sys.exit(app.exec())

