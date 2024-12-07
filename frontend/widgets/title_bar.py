from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QPoint


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Reference to the main window
        self.dragging = False
        self.offset = QPoint()
        self.setFixedHeight(40)

        # Layout for the title bar
        title_layout = QHBoxLayout(self)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.title_label = QLabel("LexBot Pro")
        self.title_label.setObjectName('TitleLabel')
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setAlignment(Qt.AlignVCenter)

        # Load icons
        minimize_icon = QIcon("static/icons/minimize4.png")
        maximize_icon = QIcon("static/icons/maximize3.png")
        close_icon = QIcon("static/icons/close2.png")

        # Minimize button
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(minimize_icon)
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.minimize_button.setFixedSize(40, 40)

        # Maximize button
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(maximize_icon)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.maximize_button.setFixedSize(40, 40)

        # Close button
        self.close_button = QPushButton()
        self.close_button.setIcon(close_icon)
        self.close_button.setObjectName('CloseButton')
        self.close_button.clicked.connect(self.parent.close)
        self.close_button.setFixedSize(40, 40)

        # Add widgets to layout
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.minimize_button)
        title_layout.addWidget(self.maximize_button)
        title_layout.addWidget(self.close_button)

    def toggle_maximize(self):
        """Maximize or restore the parent window."""
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        """Start dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """Handle dragging."""
        if self.dragging:
            self.parent.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        """Stop dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = False
