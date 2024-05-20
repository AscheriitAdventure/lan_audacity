from scapy.all import *
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout

from _src._vues.vues_obj import DynamicsDeviceView
from _src._archives.mdl_obj import Device

class DynamicsDeviceCtrlr:
    def __init__(self, model: Device, view: DynamicsDeviceView):
        self.model = model
        self.view = view

    def valid_obj(self, hostname, ipv4, mask, mac):
        # Valider l'enregistrement des informations
        try:
            self.model.name = hostname
            self.model.ipv4 = ipv4
            self.model.mask = mask
            self.model.mac = mac
            self.view.show_success('Les données ont été actualisées.')
        except ValueError as e:
            self.view.show_error(str(e))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Formulaire - mvc')

        mdl = Device(ip='192.168.90.2', mask='255.255.255.0')

        layout = QGridLayout()
        self.setLayout(layout)

        view = DynamicsDeviceView(self)
        layout.addWidget(view, 0, 0, padx=10, pady=10)

        ctrlr = DynamicsDeviceCtrlr(mdl, view)
        view.set_ctrlr(ctrlr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
