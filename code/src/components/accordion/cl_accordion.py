from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout, QLabel, QWidget

from src.components.accordion.cl_accordion_section import AccordionSection

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
