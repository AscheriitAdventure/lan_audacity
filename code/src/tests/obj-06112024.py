from qtpy.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFrame,
    QScrollArea,
    QSizePolicy,
    QLabel,
)
from qtpy.QtCore import (
    Qt,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QAbstractAnimation,
)
import sys


class AccordionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.sections = []

        # Style
        self.setStyleSheet(
            """
            QPushButton {
                padding: 8px;
                text-align: left;
                background-color: #f0f0f0;
                border: none;
                border-bottom: 1px solid #ddd;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QFrame {
                background-color: white;
                border: none;
            }
        """
        )

    def add_section(self, title, content_widget=None):
        """
        Ajoute une section à l'accordéon.

        Args:
            title (str): Le titre de la section
            content_widget (QWidget, optional): Le widget de contenu. Si None, la section sera vide.
        """
        # Si aucun contenu n'est fourni, créer un widget vide
        if content_widget is None:
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            empty_label = QLabel("Section vide")
            empty_label.setAlignment(Qt.AlignCenter)
            content_layout.addWidget(empty_label)

        section = AccordionSection(title, content_widget)
        self.sections.append(section)
        self.layout.addWidget(section)
        return section


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


# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create main window
    window = QWidget()
    window.setWindowTitle("Exemple d'Accordéon")
    main_layout = QVBoxLayout(window)

    # Create accordion
    accordion = AccordionWidget()

    # Add sections with and without content
    # Section avec contenu
    content1 = QWidget()
    content_layout = QVBoxLayout(content1)
    for j in range(3):
        btn = QPushButton(f"Bouton {j+1}")
        content_layout.addWidget(btn)
    accordion.add_section("Section 1 (avec contenu)", content1)

    # Section sans contenu
    accordion.add_section("Section 2 (sans contenu)")

    # Autre section avec contenu
    content3 = QWidget()
    content_layout = QVBoxLayout(content3)
    label = QLabel("Contenu de la section 3")
    label.setAlignment(Qt.AlignCenter)
    content_layout.addWidget(label)
    accordion.add_section("Section 3 (avec contenu)", content3)

    main_layout.addWidget(accordion)

    # Show window
    window.resize(400, 600)
    window.show()

    sys.exit(app.exec())
