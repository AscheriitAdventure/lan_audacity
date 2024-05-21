import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import qtawesome as qta


class IconTest(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Test")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.load_icon()

    def load_icon(self):
        with open(
                "/data/icon_list.json"
        ) as f:
            data = json.load(f)
        for icon in data:
            button = QPushButton(icon["name"])
            icon = qta.icon(*icon["platform_and_name"])
            button.setIcon(icon)
            self.layout.addWidget(button)


if __name__ == "__main__":
    app = QApplication([])
    window = IconTest()
    window.show()
    app.exec_()
