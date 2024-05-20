import sys

from PyQt5.QtWidgets import QApplication
from _class._prod._views import TabsView, Window
from _class._prod._mdls import NetworkManager

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = NetworkManager('192.168.1.0/24')  # Utilisation de NetworkManager
    vue = TabsView()
    window = Window(model, vue)
    window.show()
    sys.exit(app.exec_())
