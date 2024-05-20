import sys

import netifaces
import nmap
import qdarkstyle
import qtawesome as qta
from PyQt6.QtCore import pyqtSignal as Signal, QThread
from PyQt6.QtWidgets import *

from _src._mdl.mdl_itm import Device


class Worker(QThread):
    work_error = Signal(str)
    work_progress = Signal(int)
    work_completed = Signal(int)

    def __init__(self, function, objectif_dsc: str):
        self.function = function
        self.work_dsc = objectif_dsc

    def run(self):
        try:
            # Exécution de la fonction asynchrone
            self.function()
        except Exception as e:
            # En cas d'erreur, émission du signal d'erreur avec le message d'erreur
            self.work_error.emit(str(e))
        else:
            # En cas de succès, émission du signal de complétion
            self.work_completed.emit(100)

class MainWindow(QMainWindow):
    work_requested = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Nmap QThread')
        self.setGeometry(100, 100, 300, 100)
        info = self.personalIP()
        if info:
            self.myDevice = Device(info.get('addr'), info.get('netmask'))

        # Création d'un widget central et d'un layout pour le widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QGridLayout(central_widget)

        # Ajout des boutons et de la barre de progression au layout central
        btn_1 = QPushButton('nmap -sn', self)
        btn_1.clicked.connect(lambda: self.portScan('-sn'))
        btn_2 = QPushButton('nmap -sP', self)
        btn_2.clicked.connect(lambda: self.portScan('-sP'))
        btn_3 = QPushButton('nmap -sP -p-', self)
        btn_3.clicked.connect(lambda: self.portScan('-sP -p-'))
        kill_icon = qta.icon('fa5s.times-circle', color='red')
        btn_kill = QPushButton(kill_icon, '', self)
        btn_kill.setFixedSize(24, 24)
        prg_bar = QProgressBar(self)

        central_layout.addWidget(btn_1, 0, 0)
        central_layout.addWidget(btn_2, 0, 1)
        central_layout.addWidget(btn_3, 0, 2)
        central_layout.addWidget(btn_kill, 1, 3)
        central_layout.addWidget(prg_bar, 1, 0, 1, 3)
    def personalIP(self) -> dict:
        for net_interface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(net_interface):
                addr_info = netifaces.ifaddresses(net_interface)[netifaces.AF_INET]
                for info in addr_info:
                    if info.get('addr') != '127.0.0.1':
                        return info
        return {}

    def portScan(self, argv: str):
        nm = nmap.PortScanner()
        nm.scan(self.myDevice.get_cidrAddress(), argv)
        print(nm[self.myDevice.ipv4Address])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
