from src.components.accordion.cl_accordion import AccordionWidget

from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from qtpy.QtCore import Qt
import sys


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
