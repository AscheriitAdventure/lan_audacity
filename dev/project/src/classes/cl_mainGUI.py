import enum
from typing import Optional, ClassVar, Any
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import inspect

from dev.project.src.lib.qt_obj import newAction, get_spcValue
# from dev.project.src.classes.cl_menu_barManager import MenuBarManager, ShortcutManager
# from dev.project.src.cl_short import IconsApp as IconsManager
# from dev.project.src.classes.configurationFile import ConfigurationFile
from dev.project.src.classes.sql_server import MySQLConnection as SQLServer
from dev.project.src.classes.cl_factory_conf_file import IconsManager, MenuBarManager, ShortcutsManager


class MainGUI(QMainWindow):

    processRunList: ClassVar[Signal] = Signal(list[Any])

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)

        self.iconsManager = IconsManager(os.getenv("ICON_FILE_RSC"))
        self.menuBarManager = MenuBarManager(os.getenv("MENUBAR_FILE"))
        self.shortcutManager = ShortcutsManager(os.getenv("KEYBOARD_FILE_RSC"))
        self.stackedWidgetList = []
        self.link_action = self.setLinkAction()

        self.loadUI()
        self.tool_uiMenu()
        self.initUI_central()

        self.initUI_menuBar()

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

    def loadUI(self):
        self.setWindowIcon(self.iconsManager.get_icon("lan_audacity"))
        self.setWindowIconText(os.getenv("APP_NAME"))

        self.setCentralWidget(self.centralWidget())
        self.setMenuBar(self.menuBar())
        self.setStatusBar(self.statusBar())
    
    def tool_uiMenu(self):
        toolsBar = QToolBar(self)
        toolsBar.setMovable(False)
        toolsBar.setFloatable(False)

        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolsBar)
    
    def initUI_central(self) -> None:
        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Primary Side Bar (Left with QWidgets)
        self.primary_side_bar = QStackedWidget(self)
        self.primary_side_bar.setMinimumWidth(100)

        # Primary Center Object (Center with Tab Widget)
        self.primary_center = QTabWidget(self)
        self.primary_center.setMinimumHeight(100)

        # Primary Panel (Bottom with Tab Widget)
        self.primary_panel = QTabWidget(self)
        self.primary_panel.setMinimumHeight(100)

        # Splitter between Primary Panel and Primary Center
        self.v_splitter = QSplitter(Qt.Orientation.Vertical)
        self.v_splitter.addWidget(self.primary_center)
        self.v_splitter.addWidget(self.primary_panel)
        self.v_splitter.setSizes([self.primary_center.height(), self.primary_panel.height()])

        # Splitter between Primary Side Bar and V Splitter
        self.h_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.h_splitter.addWidget(self.primary_side_bar)
        self.h_splitter.addWidget(self.v_splitter)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.h_splitter)
        self.central_widget.setLayout(layout)
    
    def init_stackedWidget(self):
        # self.networkExplorer = NetworkExplorer(self)
        self.networkExplorer = QWidget(self)
        # self.dlcExplorer = DLCExplorer(self)
        self.dlcExplorer = QWidget(self)
        # self.fileExplorer = FileExplorer(self)
        self.fileExplorer = QWidget(self)

        self.primary_side_bar.addWidget(self.fileExplorer)
        self.primary_side_bar.addWidget(self.networkExplorer)
        self.primary_side_bar.addWidget(self.dlcExplorer)

        self.primary_side_bar.setCurrentIndex(0)

    def initUI_menuBar(self):
        data_obj = self.menuBarManager.file_data
        for menu in data_obj:
            menu_obj = self.menuBar().addMenu(menu["title"])
            for action in menu["actions"]:
                logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {action}")
                z = {"parent": self, "text": action["name"]}
                if slot := get_spcValue(self.link_action, "name_acte", action["name_low"], True):
                    z["slot"] = slot
                if shortcut := self.shortcutManager.get_shortcut(action["shortcut_name"]):
                    z["shortcut"] = shortcut  
                if icon := self.iconsManager.get_icon(action["icon_name"]):
                    z["icon"] = icon
                if "status_tip" in action and action["status_tip"]:
                    z["tip"] = action["status_tip"]
                q_action = newAction(**z)
                menu_obj.addAction(q_action)
                if action["name_low"] == ("save_project" or "exit"):
                    menu_obj.addSeparator()
                
    def setStackedWidget(self, index: int) -> None:
        self.primary_side_bar.setCurrentIndex(index)
    
    def add_widgetInStackedWidget(self, widget: QWidget) -> None:
        self.primary_side_bar.addWidget(widget)

    def fileExplorerAction(self) -> None:
        self.setStackedWidget(0)
    
    def netExplorerAction(self) -> None:
        self.setStackedWidget(1)
########################################################################################
"""
    Remarques:
        Bon je me débrouille pas trop mal pour le moment, j'ai réussi à mettre en place une disposition de fenêtre pas trop mal.
        Maintenant place au défi de la gestion des signaux, des slots, des threads, des datas.

        Le fil rouge de cette application est de l'environnement du Réseau Informatique et Télécom (OSI Layer 1-4).
        L'objectif est que à partir d'un fichier JSON ou YAML, on puisse récupérer les extensions nécessaire pour pouvoir utiliser 
        le SNMP, par conséquent bien organiser les données est une priorité.
    Notes:
        1 click Gauche: sélectionner un élément
        2 click Gauche: ouvrir un élément
        1 click Droit: ouvrir un menu contextuel
    Objectifs:

"""
