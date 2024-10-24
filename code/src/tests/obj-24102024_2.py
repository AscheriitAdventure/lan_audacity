from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget, QApplication
from qtpy.QtCore import Qt
import sys


class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Créer un QTableWidget avec 5 colonnes
        self.table = QTableWidget(10, 5)
        self.table.setHorizontalHeaderLabels(['IPv4', 'Name', 'Mac Address', 'Status', 'Vendor'])

        # Remplir avec des données fictives (exemple)
        data = [
            ("192.168.90.100", "intranet.eyrein2.local", "00:50:56:08:07:16", "CONNECTED", "VMware"),
            ("192.168.90.104", "EY-116.EYREIN2.local", "A4:AE:11:14:99:29", "CONNECTED", "HP"),
            ("192.168.90.105", "EY-164.EYREIN2.local", "50:81:40:98:CB:B9", "CONNECTED", "LiteON"),
            # Ajoute d'autres lignes de données ici ...
        ]

        for row, (ip, name, mac, status, vendor) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(ip))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(mac))
            self.table.setItem(row, 3, QTableWidgetItem(status))
            self.table.setItem(row, 4, QTableWidgetItem(vendor))

        # Configurer le clic sur l'en-tête pour trier
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

        # Activer le tri interactif
        self.table.setSortingEnabled(True)

        # Layout pour afficher le widget
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def onHeaderClicked(self, logicalIndex):
        # Cette méthode est appelée lorsqu'un utilisateur clique sur une en-tête de colonne
        order = self.table.horizontalHeader().sortIndicatorOrder()
        self.table.sortItems(logicalIndex, order)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExampleApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
