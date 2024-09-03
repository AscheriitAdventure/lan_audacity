import os
import logging
from typing import Any

from qtpy.QtWidgets import *
from qtpy.QtGui import QFont
from qtpy.QtCore import Qt

from src.classes.languageApp import LanguageApp
from src.classes.iconsApp import IconsApp
from src.classes.lanAudacity import LanAudacity


class FormDialog(QDialog):
    def __init__(
            self,
            title_form: str,
            ext_obj: Any = None,
            lang_manager: LanguageApp = None,
            icon_manager: IconsApp = None,
            title_window: str = "Setup",
            parent=None
    ) -> None:
        super().__init__(parent)
        self.extObj = ext_obj
        self.langManager = lang_manager
        self.iconManager = icon_manager
        self.setWindowTitle(title_window)

        self.forms_obj = self.set_formObj()  # Liste des cases remplissables
        self.fields = {}  # Zone de stockage des valeurs

        # Layout
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Title
        self.title = QLabel(title_form)
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(self.title, 0, 0, 1, 3)

        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(sep, 1, 0, 1, 3)

        # Initialize form UI
        self.formUI()

    def formUI(self) -> None:
        for i, obj in enumerate(self.forms_obj):
            label = QLabel(obj["n_label"])
            self.layout.addWidget(label, i + 2, 0)
            field = QLineEdit(self)
            field.setPlaceholderText(obj["n_placeholder"])
            if obj["n_text"]:
                field.setText(obj["n_text"])
            if obj["required"]:
                field.setStyleSheet("border: 1px solid red;")
            self.layout.addWidget(field, i + 2, 1)
            self.fields[obj["n_obj"]] = field

        # Validate button
        self.validate_button = QPushButton("Validate")
        self.layout.addWidget(self.validate_button, len(self.forms_obj) + 2, 2, alignment=Qt.AlignCenter)
        self.validate_button.clicked.connect(self.validate_form)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, len(self.forms_obj) + 2, 0, alignment=Qt.AlignCenter)
        self.cancel_button.clicked.connect(self.reject)

    def set_formObj(self) -> list:
        raise NotImplementedError("Subclasses should implement this method.")

    def validate_form(self):
        all_filled = True
        for obj in self.forms_obj:
            if obj["required"] and not self.fields[obj["n_obj"]].text():
                all_filled = False
                break

        if all_filled:
            # Message d'information que tous les champs ont été saisis
            QMessageBox.information(self, "Form Valid", "All required fields are filled.")
            self.accept()
        else:
            # Message d'erreur
            QMessageBox.critical(self, "Form Invalid", "Please fill in all required fields.")

    def get_data(self):
        data = {}
        for key, field in self.fields.items():
            if not isinstance(field, QLineEdit):
                logging.error(f"Field {key} is not a QLineEdit instance but a {type(field).__name__}")
                continue
            data[key] = field.text()
        return data


class NNetwork(FormDialog):
    def __init__(self, ext_obj: LanAudacity = None, lang_manager: LanguageApp = None, icon_manager: IconsApp = None,
                 parent=None):
        super().__init__("New Network", ext_obj=ext_obj, lang_manager=lang_manager, icon_manager=icon_manager, parent=parent)
    
    def set_formObj(self) -> list:
        data = [
            {
                "n_label": "Network Name:",
                "n_obj": "network_name",
                "n_text": "New Network",
                "n_placeholder": "Network Name",
                "required": False
            },
            {
                "n_label": "Network IPv4:",
                "n_obj": "ipv4",
                "n_text": "192.168.0.0",
                "n_placeholder": "127.0.0.0",
                "required": True
            },
            {
                "n_label": "Network Mask IPv4:",
                "n_obj": "mask_ipv4",
                "n_text": "255.255.255.0",
                "n_placeholder": "255.0.0.0",
                "required": True
            },
            {
                "n_label": "Network IPv6:",
                "n_obj": "ipv6",
                "n_text": None,
                "n_placeholder": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                "required": False
            },
            {
                "n_label": "Network Gateway:",
                "n_obj": "gateway",
                "n_text": None,
                "n_placeholder": "127.0.0.0",
                "required": False
            },
            {
                "n_label": "Network DNS:",
                "n_obj": "dns",
                "n_text": None,
                "n_placeholder": "127.0.0.0",
                "required": False
            },
            {
                "n_label": "Network DHCP:",
                "n_obj": "dhcp",
                "n_text": None,
                "n_placeholder": "127.0.0.0",
                "required": False
            }
        ]
        return data

    def get_data(self) -> dict:
        data = super().get_data()
        data["path"] = os.path.normpath(os.path.join(self.extObj.absPath, "db", "interfaces"))
        return data
        



class NProject(FormDialog):
    def __init__(self, ext_obj: Any = None, lang_manager: LanguageApp = None, icon_manager: IconsApp = None,
                 parent=None):
        super().__init__(
            "New Project",
            ext_obj=ext_obj,
            lang_manager=lang_manager,
            icon_manager=icon_manager,
            parent=parent
        )

    def set_formObj(self) -> list:
        data = [
            {
                "n_label": "Project Name:",
                "n_obj": "project_name",
                "n_text": None,
                "n_placeholder": "Project Name",
                "required": True
            },
            {
                "n_label": "Project Path:",
                "n_obj": "save_path",
                "n_text": None,
                "n_placeholder": "Project Path",
                "required": True
            },
            {
                "n_label": "Project Author:",
                "n_obj": "author",
                "n_text": None,
                "n_placeholder": "Project Author",
                "required": False
            }
        ]
        return data

    def formUI(self) -> None:
        for i, obj in enumerate(self.forms_obj):
            label = QLabel(obj["n_label"])
            self.layout.addWidget(label, i + 2, 0)
            field = QLineEdit(self)
            field.setPlaceholderText(obj["n_placeholder"])
            if obj["n_text"]:
                field.setText(obj["n_text"])
            if obj["required"]:
                field.setStyleSheet("border: 1px solid red;")
            self.layout.addWidget(field, i + 2, 1)
            self.fields[obj["n_obj"]] = field

            if obj["n_label"] == "Project Path:":
                field.setReadOnly(True)
                self.browse_button = QPushButton()
                self.browse_button.setIcon(self.iconManager.get_icon("folder_open"))
                self.browse_button.setToolTip("Select Save Path")
                self.layout.addWidget(self.browse_button, i + 2, 2)
                self.browse_button.clicked.connect(self.browse_folder)

        # Validate button
        self.validate_button = QPushButton("Validate")
        self.layout.addWidget(self.validate_button, len(self.forms_obj) + 2, 2, alignment=Qt.AlignCenter)
        self.validate_button.clicked.connect(self.validate_form)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.layout.addWidget(self.cancel_button, len(self.forms_obj) + 2, 0, alignment=Qt.AlignCenter)
        self.cancel_button.clicked.connect(self.reject)

    def browse_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Save Path", "", options=options)
        if directory:
            self.fields["save_path"].setText(directory)
            print("Save Path selected: ", directory)


class NDevice(FormDialog):
    def __init__(self, ext_obj: LanAudacity = None, lang_manager: LanguageApp = None, icon_manager: IconsApp = None,
                 parent=None):
        super().__init__(
            "New Device",
            ext_obj=ext_obj,
            lang_manager=lang_manager,
            icon_manager=icon_manager,
            parent=parent
        )

    def set_formObj(self) -> list:
        data = [
            {
                "n_label": "Device Name:",
                "n_obj": "device_name",
                "n_text": "Device 1",
                "n_placeholder": "Device Name",
                "required": False
            },
            {
                "n_label": "Device IPv4:",
                "n_obj": "ipv4",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": True
            },
            {
                "n_label": "Device Mask IPv4:",
                "n_obj": "mask_ipv4",
                "n_text": None,
                "n_placeholder": "255.0.0.0",
                "required": True
            },
            {
                "n_label": "Device IPv6:",
                "n_obj": "ipv6",
                "n_text": None,
                "n_placeholder": "::1",
                "required": False
            },
            {
                "n_label": "Device Mask IPv6:",
                "n_obj": "mask_ipv6",
                "n_text": None,
                "n_placeholder": "ffff:ffff:ffff:ffff::",
                "required": False
            },
            {
                "n_label": "Device Type:",
                "n_obj": "device_type",
                "n_text": None,
                "n_placeholder": "Router",
                "required": False
            },
            {
                "n_label": "Device Model:",
                "n_obj": "device_model",
                "n_text": None,
                "n_placeholder": "Cisco",
                "required": False
            },
            {
                "n_label": "Device Brand:",
                "n_obj": "device_brand",
                "n_text": None,
                "n_placeholder": "Linksys",
                "required": False
            },
            {
                "n_label": "Device MAC:",
                "n_obj": "device_mac",
                "n_text": None,
                "n_placeholder": "00:00:00:00:00:00",
                "required": False
            },
            {
                "n_label": "Device Gateway:",
                "n_obj": "device_gateway",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": False
            },
            {
                "n_label": "Device DNS:",
                "n_obj": "device_dns",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": False
            },
            {
                "n_label": "Device DHCP:",
                "n_obj": "device_dhcp",
                "n_text": None,
                "n_placeholder": "127.0.0.1",
                "required": False
            },
        ]
        return data