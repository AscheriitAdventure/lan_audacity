import os
import sys
import logging
import logging.config
import json
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QStatusBar, QLineEdit, QToolBar, QAction,
    QStackedWidget, QVBoxLayout, QSizePolicy,
    QDialog, QMessageBox, QSplitter
)
from qtpy.QtCore import Qt
from qtpy.QtGui import QScreen

from src.models.configuration_file import ConfigurationFile
from src.models.network import Network
from src.models.language_app import LanguageApp
from src.models.shortcut_app import ShortcutApp
from src.models.icons_app import IconsApp
from src.models.lan_audacity import LanAudacity
from src.models.menu_bar_app import MenuBarApp

from src.views.forms_app import NProject
from src.views.tabs_app import TabFactoryWidget as Tab, PreferencesTabView, GeneralTabsView
from src.views.prm_sd_pnl import FlsExpl, NetExpl, GeneralSidePanel


def current_dir():
    try:
        curr_path = os.getcwd()
        return curr_path
    except Exception as e:
        logging.error(
            f"Une erreur s'est produite lors de l'obtention du répertoire de travail actuel : {e}"
        )
        return "Analyse Erreur"


def get_spcValue(liste_add: list, arg_1: str, obj_src: str) -> dict:
    for obj_dict in liste_add:
        if obj_dict[arg_1] == obj_src:
            return obj_dict
    return {}


class MainApp(QMainWindow):
    def __init__(self, software_manager: ConfigurationFile, parent=None) -> None:
        super().__init__(parent)
        # Other Information
        self.prj_ls = []
        self.link_action = self.setLinkAction()
        # Software Information
        self.softwareManager = software_manager
        # Data Language Manager
        self.langManager = LanguageApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['translate_app']['path']}"
            )
        )
        # Data Shortcut Manager
        self.shortcutManager = ShortcutApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['shortcuts_app']['path']}"
            )
        )
        # Data Icon Manager
        self.iconsManager = IconsApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['icons_app']['path']}"
            )
        )
        # Data MenuBar Manager
        self.menuBarManager = MenuBarApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['conf']['navBar_app']['path']}"
            )
        )

        # Set the Window title
        self.setWindowTitle(self.softwareManager.data["system"]["name"])
        # Set the Window icon
        self.setWindowIcon(self.iconsManager.get_icon("lan_audacity"))
        # Set the Window Size
        self.setGeometry(100, 100, int(1920/2), int(1080/2))
        # Center the window
        self.centerWindow()
        # Set the navBar
        self.initUI_menu()
        # Set the Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Setting the GUI Information
        self.initUI_central()
        self.initUI_central()

        self.show()

    def setLinkAction(self) -> list:
        return [
            {
                "name_acte": "new_project",
                "trigger": self.newProjectAction
            },
            {
                "name_acte": "open_project",
                "trigger": self.openProjectAction
            },
            {
                "name_acte": "save_project",
                "trigger": self.saveProjectAction
            },
            {
                "name_acte": "save_as_project",
                "trigger": self.saveAsProjectAction
            },
            {
                "name_acte": "close_project",
                "trigger": self.closeProjectAction
            },
            {
                "name_acte": "exit",
                "trigger": self.quitAction
            },
            {
                "name_acte": "file_explorer",
                "trigger": self.fileExplorerAction
            },
            {
                "name_acte": "net_explorer",
                "trigger": self.netExplorerAction
            },
            {
                "name_acte": "extension",
                "trigger": self.extensionAction
            },
            {
                "name_acte": "user",
                "trigger": self.userAction
            },
            {
                "name_acte": "preferences",
                "trigger": self.preferencesAction
            },
            # {
            #     "name_acte": "language",
            #     "trigger": self.openLanguage
            # },
            # {
            #     "name_acte": "shortcut_key",
            #     "trigger": self.openShortcutKey
            # },
            # {
            #     "name_acte": "notification",
            #     "trigger": self.openNotification
            # },
            # {
            #     "name_acte": "open_terminal",
            #     "trigger": self.openTerminal
            # },
        ]

    def centerWindow(self) -> None:
        # Obtenir la géométrie de l'écran
        screen_geometry = QScreen.availableGeometry(QApplication.primaryScreen())

        # Obtenir la géométrie de la fenêtre
        window_geometry = self.geometry()

        # Calculer la position pour centrer la fenêtre
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Déplacer la fenêtre
        self.move(x, y)

    def initUI_menu(self) -> None:
        # Add toolbars
        infobar = QToolBar(self)
        # Set the toolbar to a fixed top position
        self.addToolBar(Qt.TopToolBarArea, infobar)
        # Add a Spacer
        spacerI = QWidget(self)
        spacerI.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        infobar.addWidget(spacerI)

        toolsbar = QToolBar(self)
        # Set the toolbar to a fixed left position
        self.addToolBar(Qt.LeftToolBarArea, toolsbar)

        commandLine = QLineEdit("Lan Audacity")
        commandLine.setAlignment(Qt.AlignCenter)
        commandLine.setClearButtonEnabled(True)
        commandLine.setAcceptDrops(True)
        commandLine.setDragEnabled(True)
        commandLine.setMinimumWidth(75)
        commandLine.setMaximumWidth(250)

        for menu in self.menuBarManager.data_manager:
            menu_obj = self.menuBar().addMenu(menu["menu"])
            for action in menu["actions"]:
                act_obj = QAction(action["name"], self)
                act_obj.setIcon(self.iconsManager.get_icon(action["icon_name"]))
                act_obj.setShortcut(
                    self.shortcutManager.get_shortcut(action["shortcut_name"])
                )
                act_obj.setStatusTip(action["status_tip"])
                dict_trig = get_spcValue(self.link_action, "name_acte", action["name_low"])
                if dict_trig != {}:
                    act_obj.triggered.connect(dict_trig['trigger'])
                menu_obj.addAction(act_obj)
                if action["name_low"] == "save_project":
                    menu_obj.addSeparator()
                elif action["name_low"] == "exit":
                    menu_obj.addSeparator()
                if menu["name"] == "edit_menu":
                    if action["name_low"] == "undo":
                        infobar.addAction(act_obj)
                    elif action["name_low"] == "redo":
                        infobar.addAction(act_obj)
                        infobar.addWidget(commandLine)
                        spacerO = QWidget()
                        spacerO.setSizePolicy(
                            QSizePolicy.Expanding, QSizePolicy.Expanding
                        )
                        infobar.addWidget(spacerO)
                if menu["name"] == "settings_menu":
                    if action["name_low"] == "notifications":
                        self.status_bar.addAction(act_obj)
                if menu["name"] == "view_menu":
                    if action["name_low"] == "extension":
                        toolsbar.addSeparator()
                    elif action["name_low"] == "user":
                        spacer = QWidget()
                        spacer.setSizePolicy(
                            QSizePolicy.Expanding, QSizePolicy.Expanding
                        )
                        toolsbar.addWidget(spacer)
                    toolsbar.addAction(act_obj)

        # Add Action to the infobar
        toggle_pSideBar = QAction(
            self.iconsManager.get_icon("toggleSideBar"),
            "Toggle Primary Side Bar",
            self,
        )
        toggle_pSideBar.setShortcut(
            self.shortcutManager.get_shortcut("toggleSidePanelView")
        )
        toggle_pSideBar.setStatusTip("Toggle Primary Side Bar")
        toggle_pSideBar.triggered.connect(self.toggle_primary_side_bar)
        infobar.addAction(toggle_pSideBar)

        toggle_pPanel = QAction(
            self.iconsManager.get_icon("togglePanel"),
            "Toggle Primary Panel",
            self,
        )
        toggle_pPanel.setShortcut(
            self.shortcutManager.get_shortcut("toggleTerminalView")
        )
        toggle_pPanel.setStatusTip("Toggle Primary Panel")
        toggle_pPanel.triggered.connect(self.toggle_primary_panel)
        infobar.addAction(toggle_pPanel)

    def initUI_central(self) -> None:
        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Primary Side Bar (Left with QWidgets)
        self.primary_side_bar = QStackedWidget(self)
        self.primary_side_bar.setMinimumWidth(100)
        self.primary_side_bar.setMaximumWidth(400)

        # Primary Center Object (Center with Tab Widget)
        self.primary_center = Tab(self.langManager, self)

        # Primary Panel (Bottom with Tab Widget)
        self.primary_panel = Tab(self.langManager, self)

        # Splitter between Primary Panel and Primary Center
        self.v_splitter = QSplitter(Qt.Vertical)
        self.v_splitter.addWidget(self.primary_center)
        self.v_splitter.addWidget(self.primary_panel)
        self.v_splitter.setSizes([self.primary_center.height(), self.primary_panel.height()])

        # Splitter between Primary Side Bar and V Splitter
        self.h_splitter = QSplitter(Qt.Horizontal)
        self.h_splitter.addWidget(self.primary_side_bar)
        self.h_splitter.addWidget(self.v_splitter)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.h_splitter)
        self.central_widget.setLayout(layout)

        # stack widget
        self.file_explorer = FlsExpl(
            title_panel="Explorer",
            tab_connect=self.primary_center,
            lang_manager=self.langManager,
            icon_manager=self.iconsManager,
            keys_manager=self.shortcutManager,
            parent=self
        )
        self.network_explorer = NetExpl(
            title_panel="Networks",
            tab_connect=self.primary_center,
            lang_manager=self.langManager,
            icon_manager=self.iconsManager,
            keys_manager=self.shortcutManager,
            parent=self
        )
        self.extends_explorer = GeneralSidePanel(
            title_panel="Extensions",
            lang_manager=self.langManager,
            icon_manager=self.iconsManager,
            keys_manager=self.shortcutManager,
            parent=self
        )
        self.primary_side_bar.addWidget(self.file_explorer)
        self.primary_side_bar.addWidget(self.network_explorer)
        self.primary_side_bar.addWidget(self.extends_explorer)

    def toggle_primary_side_bar(self) -> None:
        if self.primary_side_bar.isVisible():
            self.primary_side_bar.hide()
        else:
            self.primary_side_bar.show()

    def toggle_primary_panel(self) -> None:
        if self.primary_panel.isVisible():
            self.primary_panel.hide()
        else:
            self.primary_panel.show()

    # Actions
    def quitAction(self) -> None:
        logging.info("End of Application")
        self.close()

    def newProjectAction(self) -> None:
        newpa = NProject(
            icon_manager=self.iconsManager,
            lang_manager=self.langManager,
            parent=self
        )
        if newpa.exec_() == QDialog.Accepted:
            data = newpa.get_data()
            nprjlan = LanAudacity(
                software_name=self.softwareManager.data['system']['name'],
                version_software=self.softwareManager.data['system']['version'],
                project_name=data["project_name"],
                save_path=data["save_path"],
                author=data["author"]
            )
            nprjlan.create_project()
            nprjlan.save_project()
            # Add the new project to the list
            self.prj_ls.append(nprjlan)
            # Add the new project to the file explorer
            self.file_explorer.extObj = f"{data["save_path"]}/{data["project_name"]}"
            self.file_explorer.set_extObjDisplay()
            self.primary_side_bar.setCurrentWidget(self.file_explorer)
            self.network_explorer.extObj = []
            self.network_explorer.set_extObjDisplay()
            # # Generate a new project

    def openProjectAction(self) -> None:
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        folder_dialog.setNameFilter("")
        folder_dialog.exec()
        folder_path = folder_dialog.selectedFiles()[0]
        if folder_path:
            project_file = os.path.join(folder_path, "lan_audacity.json")
            if os.path.exists(project_file):
                with open(project_file, "r") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError as e:
                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setWindowTitle("ERROR")
                        msg_box.setInformativeText(f"Failed to load project file: {e}")
                        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
                        msg_box.exec()
                        return
                try:
                    nprjlan = LanAudacity(
                        software_name=data["software"],
                        version_software=data["version"],
                        project_name=os.path.basename(folder_path),
                        save_path=folder_path,
                        author=data["author"]
                    )
                except KeyError as e:
                    msg_box = QMessageBox(self)
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setWindowTitle("ERROR")
                    msg_box.setInformativeText(f"Missing key in project file: {e}")
                    msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
                    msg_box.exec()
                    return
                if data["networks"] is not None:
                    for network in data["networks"]["obj_ls"]:
                        network_file = os.path.join(folder_path, network["path"])
                        if os.path.exists(network_file):
                            with open(network_file, "r") as file:
                                try:
                                    data_network = json.load(file)
                                except json.JSONDecodeError as e:
                                    msg_box = QMessageBox(self)
                                    msg_box.setIcon(QMessageBox.Warning)
                                    msg_box.setWindowTitle("ERROR")
                                    msg_box.setInformativeText(f"Failed to load network file: {e}")
                                    msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
                                    msg_box.exec()
                                    return
                            try:
                                net0X = Network(
                                    network_ipv4=data_network["ipv4"],
                                    network_mask_ipv4=data_network["mask_ipv4"],
                                    save_path=data_network["abs_path"],
                                    network_name=data_network["name"],
                                    network_ipv6=data_network["ipv6"],
                                    network_gateway=data_network["gateway"],
                                    network_dns=data_network["dns"],
                                    network_dhcp=data_network["dhcp"],
                                    uuid_str=data_network["uuid"]
                                )
                            except KeyError as e:
                                msg_box = QMessageBox(self)
                                msg_box.setIcon(QMessageBox.Warning)
                                msg_box.setWindowTitle("ERROR")
                                msg_box.setInformativeText(f"Missing key in network file: {e}")
                                msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
                                msg_box.exec()
                                return
                            net0X.date_unix = data_network["date_unix"]
                            nprjlan.add_network(net0X)
                nprjlan.open_project()
                self.prj_ls.append(nprjlan)
                self.file_explorer.extObj = folder_path
                self.file_explorer.set_extObjDisplay()
                self.primary_side_bar.setCurrentWidget(self.file_explorer)
                self.network_explorer.extObj = nprjlan
                self.network_explorer.set_extObjDisplay()
            else:
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("ERROR")
                msg_box.setInformativeText("lan_audacity.json not found in the selected directory.")
                msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
                msg_box.exec()

    def saveProjectAction(self) -> None:
        logging.debug("Save Action...")
        # Save the project

    def saveAsProjectAction(self) -> None:
        logging.debug("Save As Action...")
        # Save the project as

    def closeProjectAction(self) -> None:
        logging.debug("Close Project Action...")
        # Close the project

    def fileExplorerAction(self) -> None:
        if self.file_explorer.isVisible() is False:
            self.primary_side_bar.setCurrentWidget(self.file_explorer)
        # Open the file explorer

    def netExplorerAction(self) -> None:
        if self.network_explorer.isVisible() is False:
            self.primary_side_bar.setCurrentWidget(self.network_explorer)
        # Show the network explorer

    def extensionAction(self) -> None:
        if self.extends_explorer.isVisible() is False:
            self.primary_side_bar.setCurrentWidget(self.extends_explorer)
        # Open the extension library

    def preferencesAction(self) -> None:
        logging.debug("Preferences Action...")
        self.primary_center.add_tab(
            tab=PreferencesTabView(
                title_panel="Preferences",
                lang_manager=self.langManager,
                icons_manager=self.iconsManager,
                parent=self
            ),
            title="Preferences"
        )
        # Open the preferences window

    def userAction(self) -> None:
        logging.debug("User Action...")
        self.primary_center.add_tab(
            tab= GeneralTabsView("User", None, self.langManager, self.iconsManager, self),
            title="User")
        # Open the user window


if __name__ == "__main__":
    softw_manager = ConfigurationFile(current_dir() + "/conf/config_app.yaml")
    path_log = (
        f"{current_dir()}/{softw_manager.data['software']['conf']['log_app']['path']}"
    )
    logs_manager = ConfigurationFile(path_log)

    logging.config.dictConfig(logs_manager.data)
    logger = logging.getLogger(__name__)

    logger.info(
        f"{softw_manager.data['system']['name']} - version {softw_manager.data['system']['version']}"
    )

    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName(softw_manager.data["system"]["name"])
    app.setApplicationVersion(softw_manager.data["system"]["version"])
    app.setOrganizationName(softw_manager.data["system"]["organization"])

    main_window = MainApp(softw_manager)
    main_window.show()

    sys.exit(app.exec_())
