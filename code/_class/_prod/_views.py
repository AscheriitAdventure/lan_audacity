import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TabsView(QTabWidget):
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

class Window(QWidget):
    def __init__(self, model, vue):
        super().__init__()

        self.setWindowTitle("Liste d'adresses IPv4")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.vue = vue
        layout.addWidget(self.vue)
        self.setLayout(layout)

        self.model = model
        self.model.set_addr()
        self.vue.update_vue(self.model.lsaddr)

        self.vue.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.vue.removeTab(index)

