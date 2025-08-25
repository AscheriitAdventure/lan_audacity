from qtpy.QtWidgets import QVBoxLayout, QPushButton, QScrollArea, QSizePolicy, QWidget
from qtpy.QtCore import QPropertyAnimation, QAbstractAnimation

class AccordionSection(QWidget):
    def __init__(self, title, content_widget):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Toggle button
        self.toggle_button = QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_content)

        # Content
        self.content_area = QScrollArea()
        self.content_area.setWidget(content_widget)
        self.content_area.setWidgetResizable(True)
        self.content_area.setMaximumHeight(0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add to layout
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.content_area)

        # Animation
        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(content_widget.sizeHint().height())

        self.is_expanded = False

    def toggle_content(self, checked):
        self.animation.setDirection(
            QAbstractAnimation.Forward if checked else QAbstractAnimation.Backward
        )
        self.animation.start()
        self.is_expanded = checked
