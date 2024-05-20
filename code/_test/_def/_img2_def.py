import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Liste d'adresses IPv4")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)  # Rend les onglets déplaçables
        self.tabs.setTabsClosable(True)  # Permet de fermer les onglets
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Définir la forme des onglets comme triangulaire
        self.tabs.setTabShape(QTabWidget.TabShape.Triangular)

        addresses = [
            "192.168.0.1",
            "10.0.0.1",
            "172.16.0.1",
            "169.254.0.1",
            "8.8.8.8"
        ]

        for address in addresses:
            tab = QWidget()
            label = QLabel(address)
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(label)
            tab.setLayout(tab_layout)
            self.tabs.addTab(tab, address)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def close_tab(self, index):
        self.tabs.removeTab(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = MaFenetre()
    fenetre.show()
    sys.exit(app.exec_())
