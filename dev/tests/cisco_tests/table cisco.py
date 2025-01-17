import sys
import asyncio
import csv
from qtpy.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from dev.project.src.classes.snmp_form import SnmpForm


class SnmpTableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SNMP Data Table")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.export_button = QPushButton("Exporter en CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_button)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["OID", "Data Type", "Value"])

        asyncio.run(self.fetch_data())

    async def fetch_data(self):
        oid = "1.3.6.1.2.1.1"
        form_snmp = {
            "ip_address": "192.168.90.250",
            "port": 161,
            "version": SnmpForm.SnmpVersion.SNMPv2c,
            "community": "ArteEyrein"
        }
        cmd_snmp = SnmpForm(**form_snmp)

        result_data = await cmd_snmp.getWalkOID(oid)

        self.table.setRowCount(len(result_data))
        for row, res in enumerate(result_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(res.oid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(res.data_type)))
            self.table.setItem(row, 2, QTableWidgetItem(str(res.rawValue)))

    def export_to_csv(self):
        with open("snmp_data.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["OID", "Data Type", "Value"])
            for row in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(row, 0).text(),
                    self.table.item(row, 1).text(),
                    self.table.item(row, 2).text()
                ])
        print("Exportation terminée !")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnmpTableApp()
    window.show()
    sys.exit(app.exec())


class SnmpTableApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SNMP Data Table")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["OID", "Data Type", "Value"])

        asyncio.run(self.fetch_data())

    async def fetch_data(self):
        oid = "1.3.6.1.2.1.1"
        form_snmp = {
            "ip_address": "192.168.90.250",
            "port": 161,
            "version": SnmpForm.SnmpVersion.SNMPv2c,
            "community": "ArteEyrein"
        }
        cmd_snmp = SnmpForm(**form_snmp)

        result_data = await cmd_snmp.getWalkOID(oid)

        self.table.setRowCount(len(result_data))
        for row, res in enumerate(result_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(res.oid)))
            self.table.setItem(row, 1, QTableWidgetItem(str(res.data_type)))
            self.table.setItem(row, 2, QTableWidgetItem(str(res.rawValue)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnmpTableApp()
    window.show()
    sys.exit(app.exec())
