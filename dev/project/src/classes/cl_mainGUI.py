from typing import Optional, ClassVar, Any, List
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect
import time
from dev.project.src.classes.cl_dialog import DynFormDialog
from dev.project.src.classes.cl_lan_audacity import LanAudacity
from dev.project.src.classes.cl_extented import IconApp, ProjectOpen
from dev.project.src.lib.qt_obj import newAction, get_spcValue
from dev.project.src.lib.template_dialog import *
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
        self.recent_projects: List = [] # Liste des projets récents
        self.stackedWidgetList: List = [] # Liste des widgets à empiler
        self.active_projects: List[LanAudacity] = [] # Liste des projets actifs

        self.loadUI()
        self.tool_uiMenu()
        self.initUI_central()

        self.initUI_menuBar()
        self.load_recent_project()

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

    ######## Native Function Operate on Windows ########
    def open_new_window(self):
        self.new_window = MainGUI()
        self.new_window.show()

    def close_current_window(self):
        self.close()

    def close_all_windows(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainGUI):
                widget.close()

    ######## Function "Exit Application" ########
    def end_application(self):
        sys.exit(QApplication.exec_())
    
    ######## Function "Open Folder Project" ########
    def open_folder_project(self):
        """Ouvre un dossier de projet et met à jour la liste des récents."""
        fd = QFileDialog(self)
        fd.setFileMode(QFileDialog.FileMode.Directory)
        fd.exec_()
    
        selected_files = fd.selectedFiles()
        if not selected_files:
            return
    
        folder_path = selected_files[0]
        logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {folder_path}")
    
        project_file = os.path.join(folder_path, "lan_audacity.json")
        if os.path.exists(project_file):
            project_name = os.path.basename(os.path.dirname(project_file))
            var_project =ProjectOpen(project_name, folder_path, time.time())
            self.add_recent_project(var_project)
            self.update_recent_menu()

            self.load_project(var_project)
        else:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {project_file} doesn't exist.")

    ######## Function to open a "recent project" ########
    def load_recent_project(self):
        """
        Load the recent project from:
        1. os.getenv("LAST_OPENED_FILE")
        2. the database (if the file is empty)
        """
        try:
            a = FactoryConfFile(os.getenv("LAST_OPENED_FILE"), FactoryConfFile.RWX.READ)
            a.read_file()
            self.recent_projects = [ProjectOpen.from_dict(i) for i in a.file_data]
            self.update_recent_menu()
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
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {a.file_data}"
            )
            a.write_file()
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
        file_menu = next(
            (menu for menu in self.menuBar().findChildren(QMenu) if menu.title() == "&File"),
            None,
        )
    
        if not file_menu:
            return
    
        recent_menu_action = next(
            (action for action in file_menu.actions() if action.menu() and action.menu().title() == "Open &Recent"),
            None,
        )
    
        if not recent_menu_action:
            return
    
        recent_menu = recent_menu_action.menu()
        recent_menu.clear()
    
        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {len(self.recent_projects)} projets récents"
        )
    
        for project in self.recent_projects:
            action = QAction(project.name, self)
            action.triggered.connect(lambda checked, p=project: self.open_recent_project(p))
            recent_menu.addAction(action)

    def open_recent_project(self, project: ProjectOpen):
        """
        Open the project from the recent project list
        """
        if project.path:
            self.add_recent_project(project) # Move to the top
            self.update_recent_menu() # Update the menu
            self.load_project(project) # Load the project

    ######## class Method for "Project" ########
    def new_project(self, debug: bool = False) -> None:
        """
        Create a new project
        """
        if debug:
            logging.debug(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {self}"
            )
        
        # Open a dialog to ask for: name of the project and the absolute path
        dialog_1 = DynFormDialog(self, False)
        dialog_1.load_form(NEW_PROJECT)
        if dialog_1.exec_() == QDialog.Accepted:
            data_1 = dialog_1.get_form_data()
            if debug:
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {data_1}"
                )

            # init the project
            z = os.path.normpath(os.path.join(data_1["save_path"], data_1["project_name"]))
            new_project = LanAudacity(directory_path=z, directory_name=data_1["project_name"])
            self.active_projects.append(new_project)

            new_project.software_id.name = os.getenv("APP_NAME")
            new_project.software_id.version = os.getenv("APP_VERSION")

            if data_1["author"]:
                new_project.add_author(data_1["author"])
            else:
                author = os.environ.get("USERNAME") or os.environ.get("USER")
                new_project.add_author(author) # add the name of the terminal user

            new_project.generate_environment(True)

            # Change the log pointer to the new log file generated
            logging.getLogger().handlers[0].stream.close()
            stream_log = os.path.join(new_project.directory_path,"logs","lan_audacity.log")
            logging.basicConfig(filename=stream_log)

            new_project.update_lan_audacity()
            po = ProjectOpen(new_project.directory_name, new_project.directory_path, time.time())
            self.add_recent_project(po)
            self.update_recent_menu()

            # Open a dialog to ask for auto-discovery mode or manual mode
            dialog_2 = DynFormDialog(self, False)
            dialog_2.load_form(DISCOVERY_MODE)

        if dialog_2.exec_() == QDialog.Accepted:
            data_2 = dialog_2.get_form_data()
            if debug:
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {data_2}"
                    )
        

        # if auto-discovery mode
            # open a window worker to start the auto-discovery
            # load the project in the GUI
        # else manual mode
            # load the project in the GUI
        # end
        
    def load_project(self, project: ProjectOpen):
        """
            Load the project in the GUI
        Args:
            project (ProjectOpen): a simple object with the project name and the absolute path
        """
        dataProjectFileName = "lan_audacity.json"
        fp, _ = QFileDialog.getExistingDirectory(self, "Open Project", project.path)
        logging.debug(
            f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {project}"
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
