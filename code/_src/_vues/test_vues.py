import qtawesome as qta
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import socket
import re


class DynamicsDeviceView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Icon de sync
        fa5_sync = qta.icon('fa5s.sync', color='blue')
        fa5_check = qta.icon('fa5s.check', color='green')
        fa5_dcheck = qta.icon('fa5s.check-double', color='green')
        fa5_cancel = qta.icon('fa5s.times', color='red')

        # Hostname
        layout.addWidget(QLabel('Hostname:'), 0, 0)
        self.hostname_edit = QLineEdit('Inconnu')
        layout.addWidget(self.hostname_edit, 0, 1)
        layout.addWidget(QPushButton(fa5_sync, ''), 0, 2)

        # IPv4
        layout.addWidget(QLabel('IPv4:'), 1, 0)
        self.ipv4_edit = QLineEdit('192.168.0.0')
        layout.addWidget(self.ipv4_edit, 1, 1)
        layout.addWidget(QPushButton(fa5_sync, ''), 1, 2)

        # Masque
        layout.addWidget(QLabel('Masque:'), 2, 0)
        self.mask_edit = QLineEdit('255.255.255.0')
        layout.addWidget(self.mask_edit, 2, 1)
        layout.addWidget(QPushButton(fa5_sync, ''), 2, 2)

        # Adresse MAC
        layout.addWidget(QLabel('Adresse MAC:'), 3, 0)
        self.mac_edit = QLineEdit('00:00:00:00:00:00')
        layout.addWidget(self.mac_edit, 3, 1)
        layout.addWidget(QPushButton(fa5_sync, ''), 3, 2)

        # Save Button
        self.apply_button = QPushButton(fa5_check, 'Vérifier')
        layout.addWidget(self.apply_button, 5, 2, alignment=Qt.AlignmentFlag.AlignRight)
        self.apply_button.clicked.connect(self.handle_apply_button)
        self.valid_btn = QPushButton(fa5_dcheck, 'Valider')
        layout.addWidget(self.valid_btn, 5, 3, alignment=Qt.AlignmentFlag.AlignRight)
        self.valid_btn.clicked.connect(self.close)
        # Cancel Button
        self.cancel_button = QPushButton(fa5_cancel, 'Annuler')
        layout.addWidget(self.cancel_button, 5, 0, alignment=Qt.AlignmentFlag.AlignRight)
        self.cancel_button.clicked.connect(self.close)
        self.show()

    def are_fields_valid(self):
        valid = True
        error_messages = []

        # Validate IPv4
        try:
            socket.inet_aton(self.ipv4_edit.text())
        except OSError:
            valid = False
            error_messages.append("IPv4 invalide")

        # Validate Subnet Mask
        if not self.is_valid_subnet_mask(self.mask_edit.text()):
            valid = False
            error_messages.append("Masque invalide")

        # Validate MAC address
        mac_pattern = re.compile("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
        if not mac_pattern.match(self.mac_edit.text()):
            valid = False
            error_messages.append("Adresse MAC invalide")

        return valid, error_messages

    def is_valid_subnet_mask(self, mask):
        try:
            ipv4_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
            match = re.match(ipv4_pattern, mask)
            if match:
                if all(0 <= int(octet) <= 255 for octet in match.groups()):
                    return True
        except ValueError:
            return False

    def handle_apply_button(self):
        valid, error_messages = self.are_fields_valid()

        if not valid:
            QMessageBox.warning(self, "Erreur de validation", "\n".join(error_messages), QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Validation réussie", "Toutes les données sont valides", QMessageBox.StandardButton.Ok)