import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QLabel

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liste d'adresses IPv4")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        addresses = [
            "192.168.0.1",
            "10.0.0.1",
            "172.16.0.1",
            "169.254.0.1",
            "8.8.8.8"
        ]

        for address in addresses:
            label = QLabel(address)
            layout.addWidget(label)

        frame.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.show()
    sys.exit(app.exec_())
