import enum
from typing import Optional, ClassVar, Any, List
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect
import time
from dev.project.src.classes.cl_extented import IconApp, ProjectOpen
from dev.project.src.lib.qt_obj import newAction, get_spcValue
from dev.project.src.classes.sql_server import MySQLConnection as SQLServer
from dev.project.src.classes.cl_factory_conf_file import (
    IconsManager,
    MenuBarManager,
    ShortcutsManager,
    FactoryConfFile,
)


class MainGUI(QMainWindow):

    # processRunList: ClassVar[Signal] = Signal(List[Any])

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)

        self.iconsManager = IconsManager(os.getenv("ICON_FILE_RSC"))
        self.menuBarManager = MenuBarManager(os.getenv("MENUBAR_FILE"))
        self.shortcutManager = ShortcutsManager(
            os.getenv("KEYBOARD_FILE_RSC")
        )  # <-- va t il rester ici ?
        self.recent_projects = []
        self.stackedWidgetList = []

        self.loadUI()
        self.tool_uiMenu()
        self.initUI_central()

        self.initUI_menuBar()

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
        self.v_splitter.setSizes(
            [self.primary_center.height(), self.primary_panel.height()]
        )

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
        for a in self.menuBarManager.menubar_object:
            if a.separator:
                self.menuBar().addSeparator()
            b = QMenu(a.title, self.menuBar())
            if a.icon:
                if isinstance(a.icon, IconApp):
                    b.setIcon(a.icon.get_qIcon())
                else:
                    logging.debug(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {a.icon}"
                    )

            self.menuBar().addMenu(b)

            if a.actions:
                for c in a.actions:
                    if c.separator:
                        b.addSeparator()
                    if c.type is None:
                        d = c.get_dict()
                        d["parent"] = self
                        logging.debug(
                            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {c}"
                        )
                        e = newAction(**d)
                        b.addAction(e)
                    else:
                        e = QMenu(c.text, self)
                        logging.debug(
                            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {e}"
                        )
                        b.addMenu(e)
            else:
                b.addSeparator()

    def setStackedWidget(self, index: int) -> None:
        if (
            self.primary_side_bar.indexOf(self.primary_side_bar.currentWidget())
            == index
        ):
            self.primary_side_bar.setWidth(0)
        elif (
            self.primary_side_bar.indexOf(self.primary_side_bar.currentWidget())
            != index
            and self.primary_side_bar.width() == 0
        ):
            self.primary_side_bar.setWidth(120)
            self.primary_side_bar.setCurrentIndex(index)
        else:
            self.primary_side_bar.setCurrentIndex(index)

    def add_widgetInStackedWidget(self, widget: QWidget) -> None:
        self.primary_side_bar.addWidget(widget)

    def open_new_window(self):
        self.new_window = MainGUI()
        self.new_window.show()

    def close_current_window(self):
        self.close()

    def close_all_windows(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainGUI):
                widget.close()

    def end_application(self):
        sys.exit(QApplication.exec_())

    ######## Function to open a "recent project" ########
    def load_recent_project(self):
        """
        Load the recent project from:
        1. os.getenv("LAST_OPENED_FILE")
        2. the database (if the file is empty)
        """
        try:
            a = FactoryConfFile(os.getenv("LAST_OPENED_FILE"), FactoryConfFile.RWX.READ)
            self.recent_projects = [ProjectOpen.from_dict(i) for i in a.file_data]
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {e}"
            )

    def save_recent_project(self):
        """
        Save the recent project from:
        1. os.getenv("LAST_OPENED_FILE")
        2. the database (if the database exists)
        """
        try:
            a = FactoryConfFile(
                os.getenv("LAST_OPENED_FILE"), FactoryConfFile.RWX.WRITE
            )
            a.file_data = [i.get_dict() for i in self.recent_projects]
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {e}"
            )

    def add_recent_project(self, project: ProjectOpen):
        """
        Add a project to the recent project list
        """
        if project in self.recent_projects:
            self.recent_projects.remove(project)
        self.recent_projects.insert(0, project)
        self.recent_projects = self.recent_projects[:10]
        self.save_recent_project()

    def update_recent_menu(self):
        """Met à jour le menu des récents avec les projets actuels."""
        mb_list = self.menuBar().findChildren(
            QMenu
        )  # liste des menus de la barre de menu
        mb_f: Optional[QMenu] = None  # type: ignore
        mb_orp: Any = None
        for mb in mb_list:
            if mb.title() == "&File":  # type: QMenu
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {mb}"
                )
                mb_f = mb
                break

        if mb_f:  # type: QMenu
            for sb in mb_f.findChildren(QMenu):
                if sb.title() == "Open &Recent":
                    logging.debug(
                        f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {sb}"
                    )
                    mb_orp = sb
                    break

        if mb_orp:
            mb_orp.clear()
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self.recent_projects.__len__()}"
            )
            for project in self.recent_projects:
                action = QAction(project.name, self)
                action.triggered.connect(
                    lambda checked, p=project: self.open_folder_project(p)
                )
                mb_orp.addAction(action)

    def open_folder_project(self):
        fd = QFileDialog(self)
        fd.setFileMode(QFileDialog.FileMode.Directory)
        fd.setNameFilter("")
        fd.exec_()

        fp = fd.selectedFiles()[0]
        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {fp}"
        )

        if fp:
            pf = os.path.join(fp, "lan_audacity.json")
            if os.path.exists(pf):

                self.add_recent_project(
                    ProjectOpen(os.path.basename(os.path.dirname(pf)), fp, time.time())
                )
                self.update_recent_menu()
                # chargement du projet dans le GUI
            else:
                logging.error(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {pf} doesn't exist."
                )

    ########################################################


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
