from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTreeView, QGridLayout, QTabWidget, QSplitter, QWidget
from PyQt5.QtCore import Qt

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Main Window")

        self.set_ui()

    def set_ui(self):
        layout = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Création des boutons de l'alphabet
        alphabet = "ABCDEFGHIJ"
        for i, letter in enumerate(alphabet):
            button = QPushButton(letter, self)
            button.setFixedSize(32, 32)
            layout.addWidget(button, i+1, 0)

        # Ajout des autres widgets
        home_button = QPushButton("Home", self)
        home_button.setFixedSize(32, 32)
        layout.addWidget(home_button, 0, 0)

        line_edit = QLineEdit(self)
        layout.addWidget(line_edit, 0, 1)

        settings_button = QPushButton("Settings", self)
        settings_button.setFixedSize(32, 32)
        layout.addWidget(settings_button, 0, 2)

        user_button = QPushButton("User", self)
        user_button.setFixedSize(32, 32)
        layout.addWidget(user_button, 0, 3)

        tree_view = QTreeView(self)
        layout.addWidget(tree_view, 1, 1, 9, 1)

        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter, 1, 2, 9, 3)

        tab_view1 = QTabWidget()
        tab_view2 = QTabWidget()
        splitter.addWidget(tab_view1)
        splitter.addWidget(tab_view2)


if __name__ == "__main__":
    app = QApplication([])
    window = CustomMainWindow()
    window.show()
    app.exec_()
