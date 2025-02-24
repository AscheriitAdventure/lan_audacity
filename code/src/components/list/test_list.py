from src.components.list.cl_list import CLIconTextU1

from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import sys


# Fonction principale pour tester CLIconTextU1
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    # Instance de CLIconTextU1
    icon_text_widget = CLIconTextU1(logger=True, toggle_icon=True, search_panel=True)

    # Création et ajout de boutons
    button1 = QPushButton("Settings")
    button2 = QPushButton("User Profile")
    button3 = QPushButton("Admin Panel")
    button4 = QPushButton("Help")
    button5 = QPushButton("Logout")
    
    icon_text_widget.add_btn(button1)
    icon_text_widget.add_btn(button2)
    icon_text_widget.add_btn(button3)
    icon_text_widget.add_btn(button4)
    icon_text_widget.add_btn(button5)

    layout.addWidget(icon_text_widget)
    window.setLayout(layout)
    window.setWindowTitle("Test CLIconTextU1")
    window.resize(300, 400)
    window.show()

    sys.exit(app.exec_())

# Appel de la fonction principale
if __name__ == "__main__":
    main()