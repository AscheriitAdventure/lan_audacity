import logging
import sys
import os, json
import qtawesome as qta
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *

from lan_audacity import LanAudacity
from primarySidePanel import NetExpl, FlsExpl, GeneralSidePanel


class NProjectDock(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")

        # layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Title
        self.title = QLabel("New Project")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.title, 0, 0, 1, 3)

        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        layout.addWidget(sep, 1, 0, 1, 3)

        # Project Name
        self.project_name_label = QLabel("Name:")
        self.project_name = QLineEdit(self)
        self.project_name.setPlaceholderText("Project Name")
        layout.addWidget(self.project_name_label, 2, 0)
        layout.addWidget(self.project_name, 2, 1)

        # Author
        self.author_label = QLabel("Author:")
        self.author = QLineEdit(self)
        self.author.setPlaceholderText("Author")
        layout.addWidget(self.author_label, 3, 0)
        layout.addWidget(self.author, 3, 1)

        # Save Path
        self.save_path_label = QLabel("Path:")
        self.save_path_button = QPushButton(self)
        self.save_path_button.setIcon(qta.icon("mdi6.folder-open-outline", color="orange"))
        self.save_path_button.setToolTip("Select Save Path")
        self.save_path_text = QLineEdit()
        self.save_path_text.setReadOnly(True)
        layout.addWidget(self.save_path_label, 4, 0)
        layout.addWidget(self.save_path_text, 4, 1)
        layout.addWidget(self.save_path_button, 4, 2)
        self.save_path_button.clicked.connect(self.select_save_path)
        self.save_path = ""

        # Validate button
        self.validate_button = QPushButton("Validate")
        layout.addWidget(self.validate_button, 5, 2, alignment=Qt.AlignCenter)
        self.validate_button.clicked.connect(self.validate_form)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.cancel_button, 5, 0, alignment=Qt.AlignCenter)
        self.cancel_button.clicked.connect(self.reject)

    def select_save_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Select Save Path", "", options=options)
        if directory:
            self.save_path = directory
            self.save_path_text.setText(self.save_path)
            print("Save Path selected: ", self.save_path)

    def validate_form(self):
        if self.project_name.text() and self.author.text() and self.save_path:
            QMessageBox.information(self, "Confirmation", "All fields are filled in.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def get_data(self):
        return {
            "project_name": self.project_name.text(),
            "author": self.author.text(),
            "save_path": self.save_path,
        }


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ls_icon = []
        self.ls_objMenuBar = []
        self.prj_ls: list[LanAudacity] = []
        self.set_lists()
        self.setWindowTitle("Lan Audacity Test")
        self.setWindowIcon(self.srchIcon("software_icon"))
        self.setGeometry(100, 100, 800, 600)

        # menu bar
        self.menuBar()

        # status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Setting window
        self.init_menu()
        self.init_centralWindow()

        self.show()

    def srchIcon(self, icon_name):
        for icon in self.ls_icon:
            if icon["name"] == icon_name:
                return icon["icon"]
        return None

    def srchKey(self, key_name):
        for key in self.ls_icon:
            if key["name"] == key_name:
                return key["shortcut"]
        return None

    def srchAction(self, action_name) -> dict:
        for menu in self.ls_objMenuBar:
            for action in menu["actions"]:
                if action["name"] == action_name:
                    obj = action
                    return obj
        return {}
    
    def set_lists(self):
        self.ls_icon = [
            {
                "name": "extensionAction",
                "icon": qta.icon("mdi6.puzzle"),
                "shortcut": "Ctrl+Shift+X",
            },
            {
                "name": "userAction",
                "icon": qta.icon("mdi6.account-settings"),
                "shortcut": "Alt+Shift+U",
            },
            {
                "name": "preferencesAction",
                "icon": qta.icon("mdi6.cog-outline"),
                "shortcut": "Alt+Shift+P",
            },
            {
                "name": "software_icon",
                "icon": qta.icon("fa5s.flag"),
                "shortcut": "Ctrl+Q",
            },
            {
                "name": "newProject",
                "icon": qta.icon("mdi6.new-box"),
                "shortcut": "Ctrl+N",
            },
            {
                "name": "openProject",
                "icon": qta.icon("mdi6.open-in-app"),
                "shortcut": "Ctrl+O",
            },
            {
                "name": "saveProject",
                "icon": qta.icon("mdi6.content-save"),
                "shortcut": "Ctrl+S",
            },
            {
                "name": "saveAsProject",
                "icon": qta.icon("mdi6.content-save-plus"),
                "shortcut": "Ctrl+Shift+S",
            },
            {
                "name": "closeProject",
                "icon": qta.icon("mdi6.folder-off"),
                "shortcut": "Ctrl+W",
            },
            {
                "name": "exit",
                "icon": qta.icon("mdi6.exit-to-app"),
                "shortcut": "Alt+F4",
            },
            {
                "name": "undoAction",
                "icon": qta.icon("fa5s.undo-alt"),
                "shortcut": "Ctrl+Z",
            },
            {
                "name": "redoAction",
                "icon": qta.icon("fa5s.redo-alt"),
                "shortcut": "Ctrl+Y",
            },
            {
                "name": "cutAction",
                "icon": qta.icon("fa5s.cut"),
                "shortcut": "Ctrl+X",
            },
            {
                "name": "copyAction",
                "icon": qta.icon("fa5s.copy"),
                "shortcut": "Ctrl+C",
            },
            {
                "name": "pasteAction",
                "icon": qta.icon("fa5s.paste"),
                "shortcut": "Ctrl+V",
            },
            {
                "name": "deleteAction",
                "icon": qta.icon("fa5s.eraser"),
                "shortcut": "Del",
            },
            {
                "name": "selectAllAction",
                "icon": qta.icon("mdi6.select-all"),
                "shortcut": "Ctrl+A",
            },
            {
                "name": "selectNoneAction",
                "icon": qta.icon("mdi6.selection-off"),
                "shortcut": "Ctrl+Shift+A",
            },
            {
                "name": "selectInverseAction",
                "icon": qta.icon("mdi6.select-inverse"),
                "shortcut": "Ctrl+I",
            },
            {
                "name": "fileExplorerAction",
                "icon": qta.icon("mdi6.folder-settings"),
                "shortcut": "Ctrl+Shift+E",
            },
            {
                "name": "netExplorerAction",
                "icon": qta.icon("mdi6.wan"),
                "shortcut": "Ctrl+Shift+N",
            },
            {
                "name": "notificationAction",
                "icon": qta.icon("mdi6.bell"),
                "shortcut": "Alt+N",
            },
            {
                "name": "translateAction",
                "icon": qta.icon("mdi6.translate"),
                "shortcut": "Ctrl+Shift+L",
            },
            {
                "name": "terminalAction",
                "icon": qta.icon("mdi6.console"),
                "shortcut": "Ctrl+Shift+ù",
            },
            {
                "name": "helpAction",
                "icon": qta.icon("mdi6.chat-question"),
                "shortcut": "F1",
            },
            {
                "name": "aboutAction",
                "icon": qta.icon("mdi6.information-variant"),
                "shortcut": "Ctrl+Shift+M",
            },
            {
                "name": "languageAction",
                "icon": qta.icon("mdi6.web"),
                "shortcut": "Alt+L",
            },
            {
                "name": "shortcutKeyAction",
                "icon": qta.icon("mdi6.keyboard-settings"),
                "shortcut": "Alt+K",
            },
        ]

        self.ls_objMenuBar = [
            {
                "name": "file_menu",
                "menu": self.menuBar().addMenu("&File"),
                "actions": [
                    {
                        "name": "new_project",
                        "action": QAction(
                            self.srchIcon("newProject"), "&New Project", self
                        ),
                        "shortcut": self.srchKey("newProject"),
                        "status_tip": "Create a new project",
                        "triggered": self.newProjectAction,
                    },
                    {
                        "name": "open_project",
                        "action": QAction(
                            self.srchIcon("openProject"),
                            "&Open Project",
                            self,
                        ),
                        "shortcut": self.srchKey("openProject"),
                        "status_tip": "Open a project",
                        "triggered": self.openProjectAction,
                    },
                    {
                        "name": "save_project",
                        "action": QAction(
                            self.srchIcon("saveProject"),
                            "&Save Project",
                            self,
                        ),
                        "shortcut": self.srchKey("saveProject"),
                        "status_tip": "Save the project",
                        "triggered": self.saveProjectAction,
                    },
                    {
                        "name": "save_as_project",
                        "action": QAction(
                            self.srchIcon("saveAsProject"),
                            "&Save As Project",
                            self,
                        ),
                        "shortcut": self.srchKey("saveAsProject"),
                        "status_tip": "Save the project as",
                        "triggered": self.saveAsProjectAction,
                    },
                    {
                        "name": "close_project",
                        "action": QAction(
                            self.srchIcon("closeProject"),
                            "&Close Project",
                            self,
                        ),
                        "shortcut": self.srchKey("closeProject"),
                        "status_tip": "Close the project",
                        "triggered": self.closeProjectAction,
                    },
                    {
                        "name": "exit",
                        "action": QAction(self.srchIcon("exit"), "&Exit", self),
                        "shortcut": self.srchKey("exit"),
                        "status_tip": "Exit the application",
                        "triggered": self.close,
                    },
                ],
            },
            {
                "name": "edit_menu",
                "menu": self.menuBar().addMenu("&Edit"),
                "actions": [
                    {
                        "name": "undo",
                        "action": QAction(self.srchIcon("undoAction"), "&Undo", self),
                        "shortcut": self.srchKey("undoAction"),
                        "status_tip": "Undo the last action",
                        "triggered": None,
                    },
                    {
                        "name": "redo",
                        "action": QAction(self.srchIcon("redoAction"), "&Redo", self),
                        "shortcut": self.srchKey("redoAction"),
                        "status_tip": "Redo the last action",
                        "triggered": None,
                    },
                    {
                        "name": "cut",
                        "action": QAction(self.srchIcon("cutAction"), "&Cut", self),
                        "shortcut": self.srchKey("cutAction"),
                        "status_tip": "Cut the selected text",
                        "triggered": None,
                    },
                    {
                        "name": "copy",
                        "action": QAction(self.srchIcon("copyAction"), "&Copy", self),
                        "shortcut": self.srchKey("copyAction"),
                        "status_tip": "Copy the selected text",
                        "triggered": None,
                    },
                    {
                        "name": "paste",
                        "action": QAction(self.srchIcon("pasteAction"), "&Paste", self),
                        "shortcut": self.srchKey("pasteAction"),
                        "status_tip": "Paste the selected text",
                        "triggered": None,
                    },
                    {
                        "name": "delete",
                        "action": QAction(
                            self.srchIcon("deleteAction"), "&Delete", self
                        ),
                        "shortcut": self.srchKey("deleteAction"),
                        "status_tip": "Delete the selected text",
                        "triggered": None,
                    },
                ],
            },
            {
                "name": "select_menu",
                "menu": self.menuBar().addMenu("&Select"),
                "actions": [
                    {
                        "name": "select_all",
                        "action": QAction(
                            self.srchIcon("selectAllAction"),
                            "&Select All",
                            self,
                        ),
                        "shortcut": self.srchKey("selectAllAction"),
                        "status_tip": "Select all text",
                        "triggered": None,
                    },
                    {
                        "name": "select_none",
                        "action": QAction(
                            self.srchIcon("selectNoneAction"),
                            "&Select None",
                            self,
                        ),
                        "shortcut": self.srchKey("selectNoneAction"),
                        "status_tip": "Select none text",
                        "triggered": None,
                    },
                    {
                        "name": "select_inverse",
                        "action": QAction(
                            self.srchIcon("selectInverseAction"),
                            "&Select Inverse",
                            self,
                        ),
                        "shortcut": self.srchKey("selectInverseAction"),
                        "status_tip": "Select inverse text",
                        "triggered": None,
                    },
                ],
            },
            {
                "name": "view_menu",
                "menu": self.menuBar().addMenu("&View"),
                "actions": [
                    {
                        "name": "file_explorer",
                        "action": QAction(
                            self.srchIcon("fileExplorerAction"),
                            "&File Explorer",
                            self,
                        ),
                        "shortcut": self.srchKey("fileExplorerAction"),
                        "status_tip": "Open file explorer",
                        "triggered": self.fileExplorerAction,
                    },
                    {
                        "name": "net_explorer",
                        "action": QAction(
                            self.srchIcon("netExplorerAction"),
                            "&Network Explorer",
                            self,
                        ),
                        "shortcut": self.srchKey("netExplorerAction"),
                        "status_tip": "Open network explorer",
                        "triggered": self.netExplorerAction,
                    },
                    {
                        "name": "extension",
                        "action": QAction(
                            self.srchIcon("extensionAction"),
                            "&Extension",
                            self,
                        ),
                        "shortcut": self.srchKey("extensionAction"),
                        "status_tip": "Show Extension Library",
                        "triggered": self.extensionAction,
                    },
                    {
                        "name": "user",
                        "action": QAction(
                            self.srchIcon("userAction"),
                            "&User",
                            self,
                        ),
                        "shortcut": self.srchKey("userAction"),
                        "status_tip": "Open Window User",
                        "triggered": self.userAction,
                    },
                    {
                        "name": "preferences",
                        "action": QAction(
                            self.srchIcon("preferencesAction"),
                            "&Preferences",
                            self,
                        ),
                        "shortcut": self.srchKey("preferencesAction"),
                        "status_tip": "Open Window Preferences",
                        "triggered": self.preferencesAction,
                    },
                ],
            },
            {
                "name": "settings_menu",
                "menu": self.menuBar().addMenu("&Settings"),
                "actions": [
                    {
                        "name": "language",
                        "action": QAction(
                            self.srchIcon("languageAction"),
                            "&Language",
                            self,
                        ),
                        "shortcut": self.srchKey("languageAction"),
                        "status_tip": "Change language",
                        "triggered": None,
                    },
                    {
                        "name": "shortcut_key",
                        "action": QAction(
                            self.srchIcon("shortcutKeyAction"),
                            "&Shortcut Key",
                            self,
                        ),
                        "shortcut": self.srchKey("shortcutKeyAction"),
                        "status_tip": "Change shortcut key",
                        "triggered": None,
                    },
                    {
                        "name": "notification",
                        "action": QAction(
                            self.srchIcon("notificationAction"),
                            "&Notification",
                            self,
                        ),
                        "shortcut": self.srchKey("notificationAction"),
                        "status_tip": "Show notification",
                        "triggered": None,
                    },
                ],
            },
            {
                "name": "terminal_menu",
                "menu": self.menuBar().addMenu("&Terminal"),
                "actions": [
                    {
                        "name": "open_terminal",
                        "action": QAction(
                            self.srchIcon("terminalAction"),
                            "&Open Terminal",
                            self,
                        ),
                        "shortcut": self.srchKey("terminalAction"),
                        "status_tip": "Open terminal",
                        "triggered": None,
                    },
                ],
            },
            {
                "name": "help_menu",
                "menu": self.menuBar().addMenu("&Help"),
                "actions": [
                    {
                        "name": "help",
                        "action": QAction(self.srchIcon("helpAction"), "&Help", self),
                        "shortcut": self.srchKey("helpAction"),
                        "status_tip": "Help",
                        "triggered": None,
                    },
                    {
                        "name": "about",
                        "action": QAction(self.srchIcon("aboutAction"), "&About", self),
                        "shortcut": self.srchKey("aboutAction"),
                        "status_tip": "About",
                        "triggered": None,
                    },
                ],
            },
        ]

    def init_menu(self):
        commandLine = QLineEdit("Lan Audacity")
        commandLine.setAlignment(Qt.AlignCenter)
        commandLine.setClearButtonEnabled(True)
        commandLine.setAcceptDrops(True)
        commandLine.setDragEnabled(True)
        commandLine.setMinimumWidth(75)
        commandLine.setMaximumWidth(250)

        for menu in self.ls_objMenuBar:
            for action in menu["actions"]:
                if action['name'] == "save_project":
                    menu["menu"].addSeparator()
                elif action['name'] == "exit":
                    menu["menu"].addSeparator()
                menu["menu"].addAction(action["action"])
                if action["shortcut"]:
                    action["action"].setShortcut(action["shortcut"])
                if action["status_tip"]:
                    action["action"].setStatusTip(action["status_tip"])
                if action["triggered"]:
                    action["action"].triggered.connect(action["triggered"])

        # Add toolbars
        infobar = QToolBar(self)
        # Set the toolbar to a fixed top position
        self.addToolBar(Qt.TopToolBarArea, infobar)
        # Add a Spacer
        spacerI = QWidget()
        spacerI.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        infobar.addWidget(spacerI)

        toolsbar = QToolBar(self)
        # Set the toolbar to a fixed left position
        self.addToolBar(Qt.LeftToolBarArea, toolsbar)

        for menu in self.ls_objMenuBar:
            if menu["name"] == "edit_menu":
                for action in menu["actions"]:
                    if action["name"] == "undo":
                        infobar.addAction(action["action"])
                    elif action["name"] == "redo":
                        infobar.addAction(action["action"])
                        infobar.addWidget(commandLine)
                        spacerO = QWidget()
                        spacerO.setSizePolicy(
                            QSizePolicy.Expanding, QSizePolicy.Expanding
                        )
                        infobar.addWidget(spacerO)
            if menu["name"] == "settings_menu":
                for action in menu["actions"]:
                    if action["name"] == "notification":
                        self.status_bar.addAction(action["action"])
            if menu["name"] == "view_menu":
                for action in menu["actions"]:
                    if action["name"] == "extension":
                        toolsbar.addSeparator()
                    elif action["name"] == "user":
                        spacer = QWidget()
                        spacer.setSizePolicy(
                            QSizePolicy.Expanding, QSizePolicy.Expanding
                        )
                        toolsbar.addWidget(spacer)
                    toolsbar.addAction(action["action"])
        
        # Add Action to the infobar
        toggle_pSideBar = QAction(qta.icon("fa5s.window-maximize",  rotated=270), "Toggle Primary Side Bar", self)
        toggle_pSideBar.setShortcut("Ctrl+B")
        toggle_pSideBar.setStatusTip("Toggle Primary Side Bar")
        toggle_pSideBar.triggered.connect(self.toggle_primary_side_bar)

        toggle_pPanel = QAction(qta.icon("fa5s.window-maximize",  rotated=180), "Toggle Primary Panel", self)
        toggle_pPanel.setShortcut("Ctrl+J")
        toggle_pPanel.setStatusTip("Toggle Primary Panel")
        toggle_pPanel.triggered.connect(self.toggle_primary_panel)

        infobar.addAction(toggle_pSideBar)
        infobar.addAction(toggle_pPanel)
    
    def init_centralWindow(self):
        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Primary Side Bar (Left with QWidgets)
        self.primary_side_bar = QStackedWidget(self)
        self.primary_side_bar.setMinimumWidth(100)
        self.primary_side_bar.setMaximumWidth(400)
        self.primary_side_bar.hide()

        # Primary Center Object (Center with Tab Widget)
        self.primary_center = QTabWidget(self)
        self.primary_center.setMinimumWidth(100)
        self.primary_center.setMinimumHeight(100)
        self.primary_center.setTabsClosable(True)
        self.primary_center.setMovable(True)

        # Primary Panel (Bottom with Tab Widget)
        self.primary_panel = QTabWidget(self)
        self.primary_panel.setMinimumHeight(100)
        self.primary_panel.setTabsClosable(True)
        self.primary_panel.setMovable(True)
        self.primary_panel.hide()

        # Splitter between Primary Panel and Primary Center
        self.v_splitter = QSplitter(Qt.Vertical)
        self.v_splitter.addWidget(self.primary_center)
        self.v_splitter.addWidget(self.primary_panel)

        # Splitter between Primary Side Bar and V Splitter
        self.h_splitter = QSplitter(Qt.Horizontal)
        self.h_splitter.addWidget(self.primary_side_bar)
        self.h_splitter.addWidget(self.v_splitter)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.h_splitter)
        self.central_widget.setLayout(layout)

        self.file_explorer = FlsExpl("File Explorer", parent=self)
        self.network_explorer = NetExpl("Network Explorer", parent=self)
        self.extends_explorer = GeneralSidePanel("Extensions Explorer", parent=self)

        self.primary_side_bar.addWidget(self.file_explorer)
        self.primary_side_bar.addWidget(self.network_explorer)
        self.primary_side_bar.addWidget(self.extends_explorer)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def toggle_primary_side_bar(self):
        if self.primary_side_bar.isVisible():
            self.primary_side_bar.hide()
        else:
            self.primary_side_bar.show()
    
    def toggle_primary_panel(self):
        if self.primary_panel.isVisible():
            self.primary_panel.hide()
        else:
            self.primary_panel.show()
    
    def dockAction(self, action):
        self.dock_obj = QDockWidget(action['name'], self)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_obj)
        self.dock_obj.show()
    
    def tabAction(self, action):
        self.tab_obj = QWidget(self)
        self.primary_center.addTab(self.tab_obj, action['name'])
        self.primary_center.setCurrentWidget(self.tab_obj)
    
    def newProjectAction(self):
        newpa = NProjectDock()
        if newpa.exec_() == QDialog.Accepted:
            data = newpa.get_data()
            nprjlan = LanAudacity("Lan Audacity", "1.1.3", data["project_name"], data["save_path"], data["author"])
            logging.info(nprjlan.create_project())
            # Add the new project to the list
            self.prj_ls.append(nprjlan)
            # Add the new project to the file explorer
            self.file_explorer.extObj = f"{data["save_path"]}/{data["project_name"]}"
            self.file_explorer.loadDisplayObj()
            self.primary_side_bar.setCurrentWidget(self.file_explorer)
            # # Add the new project to the network explorer
            if nprjlan.networks is not None:
                # Add the network list to the network explorer
                self.network_explorer.extObj = nprjlan
                self.network_explorer.loadDisplayObj()
            else:
                # Show a message that there is no network
                QMessageBox.information(self, "No Network", "There is no network available.")
            # # Generate a new project
    
    def openProjectAction(self):
        directory_project = QFileDialog.getExistingDirectory(self, "Open Project", os.getcwd())
        if directory_project:
            project_file = os.path.join(directory_project, "lan_audacity.json")
            if os.path.exists(project_file):
                with open(project_file, "r") as file:
                    data = json.load(file)
                nprjlan = LanAudacity(
                    "Lan Audacity", 
                    "1.1.3", 
                    os.path.basename(directory_project),
                    directory_project)
                logging.info(nprjlan.open_project())
                self.prj_ls.append(nprjlan)
                self.file_explorer.extObj = directory_project
                self.file_explorer.loadDisplayObj()
                self.primary_side_bar.setCurrentWidget(self.file_explorer)
                if nprjlan.networks is not None:
                    self.network_explorer.extObj = nprjlan
                    self.network_explorer.loadDisplayObj()
                else:
                    QMessageBox.information(self, "No Network", "There is no network available.")
                # Charger l'arborescence dans le QTreeView
            else:
                QMessageBox.warning(self, "Error", "lan_audacity.json not found in the selected directory.")
        # Open a project
    
    def saveProjectAction(self):
        self.dockAction(self.srchAction("save_project"))
        # Save the project
    
    def saveAsProjectAction(self):
        self.dockAction(self.srchAction("save_as_project"))
        # Save the project as
    
    def closeProjectAction(self):
        self.dockAction(self.srchAction("close_project"))
        # Close the project
    
    def fileExplorerAction(self):
        if self.file_explorer.isVisible():
            self.toggle_primary_side_bar()
        else:
            self.primary_side_bar.setCurrentWidget(self.file_explorer)
        # Open the file explorer
    
    def netExplorerAction(self):
        if self.network_explorer.isVisible():
            self.toggle_primary_side_bar()
        else:
            self.primary_side_bar.setCurrentWidget(self.network_explorer)
        # Show the network explorer
    
    def extensionAction(self):
        if self.extends_explorer.isVisible():
            self.toggle_primary_side_bar()
        else:
            self.primary_side_bar.setCurrentWidget(self.extends_explorer)
        # Open the extension library
    
    def preferencesAction(self):
        self.tabAction(self.srchAction("preferences"))
        # Open the preferences window
    
    def userAction(self):
        self.tabAction(self.srchAction("user"))
        # Open the user window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
