import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import uuid
import nmap


class NetworkManager:
    def __init__(self, adressecidr: str):
        self.__uuid = uuid.uuid4()
        self.__adressecidr: str = adressecidr
        self.__lsaddr: list = []

    @property
    def uuid(self):
        return self.__uuid

    @property
    def addrCIDR(self):
        return self.__adressecidr

    @addrCIDR.setter
    def addrCIDR(self, value: str):
        self.__adressecidr = value

    @property
    def lsaddr(self):
        return self.__lsaddr


    def set_addr(self):
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=self.__adressecidr, arguments='-sn')
            self.__lsaddr = nm.all_hosts()
        except nmap.PortScannerError:
            print('Erreur lors du scan du réseau.')


class MaVue(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setMovable(True)  # Rend les onglets déplaçables
        self.setTabsClosable(True)  # Permet de fermer les onglets

    def update_vue(self, adresses):
        self.clear()
        for adresse in adresses:
            tab = QWidget()
            label = QLabel(adresse)
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(label)
            tab.setLayout(tab_layout)
            self.addTab(tab, adresse)


class MaFenetre(QWidget):
    def __init__(self, model, vue):
        super().__init__()

        self.setWindowTitle("Liste d'adresses IPv4")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.vue = vue
        layout.addWidget(self.vue)
        self.setLayout(layout)

        self.model = model
        self.model.set_addr()  # Appel à la méthode pour scanner le réseau
        self.vue.update_vue(self.model.lsaddr)  # Utilisation de lsaddr

        self.vue.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.vue.removeTab(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = NetworkManager('192.168.0.0/24')  # Utilisation de NetworkManager
    vue = MaVue()
    fenetre = MaFenetre(model, vue)
    fenetre.show()
    sys.exit(app.exec_())
