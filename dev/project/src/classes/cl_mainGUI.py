from typing import Optional, ClassVar, Any, List
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect
import time
from dev.project.src.classes.cl_stacked_objects import SDFSP
from dev.project.src.lib.template_tools_bar import *
from dev.project.src.classes.cl_dialog import DynFormDialog
from dev.project.src.classes.cl_lan_audacity import LanAudacity, Interfaces
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

    processRunList: ClassVar[Signal] = Signal(list)

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
        self.initUI_central()

        self.initUI_menuBar()
        self.load_recent_project()
        # imposer un dialog pour ouvrir un projet sinon il y aura des problème de chargements
        self.init_stackedWidget()

    def loadUI(self):
        self.setWindowIcon(self.iconsManager.get_icon("lan_audacity"))
        self.setWindowIconText(os.getenv("APP_NAME"))

        self.setCentralWidget(self.centralWidget())
        self.setMenuBar(self.menuBar())
        self.setStatusBar(self.statusBar())

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
        stacks = [LAN_EXPLORER, FILES_EXPLORER, DLC_EXPLORER]
        for stack in stacks:
            # Create the widget
            sdfsp = SDFSP(debug=True, parent=self)
            self.primary_side_bar.addWidget(sdfsp)
            self.stackedWidgetList.append(sdfsp)

            if self.active_projects != []:
                ao = self.active_projects[0]
                for field in stack["fields"]:
                    if field_form := field.get("form_list"):
                        if field_form == 'tree-file':
                            field["widget_data"] = ao.directory_path
                            field['title'] = ao.directory_name
                            # field['actions'].append()
                        elif field_form == 'tree':
                            field["widget_data"] = []
                            # field['actions'].append()
                        elif field_form == 'list-btn':
                            field["widget_data"] = []
                            # field['actions'].append()
                    else:
                        logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {field_form} Unknown")
                        continue
            else:
                # Add Data and/or Objects in the widget
                sdfsp.load_stack_data(stack)

        self.primary_side_bar.setCurrentIndex(0)
    
    def update_stackedWidget(self, index: int, data: dict):
        """
        Met à jour les données d'un widget et de ses fields
       Args:
            index (int): Index du widget à mettre à jour
            data (dict): Données à mettre à jour
        """
        try:
            # Récupérer le widget SDFSP correspondant à l'index
            sdfsp: SDFSP = self.stackedWidgetList[index]

            # Pour chaque field dans le widget
            for field in sdfsp.active_fields:
                form_type = field.get('form_list')
            
                # Mettre à jour selon le type de formulaire
                if form_type == 'tree-file':
                    # Si c'est un explorateur de fichiers
                    if field['title']:
                        # Mettre à jour le titre avec le nom du projet
                        field['widget'].findChild(QLabel).setText(data['directory_name'].upper())
                        # Mettre à jour le tooltip
                        field['widget'].setToolTip(f"Explorateur de Réseaux de {data['directory_name']}")
                        
                        # Mettre à jour l'arborescence
                        tree_view = field['widget'].findChild(QTreeView)
                        if tree_view:
                            model = QFileSystemModel()
                            model.setRootPath(data['directory_path'])
                            model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllDirs | QDir.Filter.Files)
                            tree_view.setModel(model)
                            tree_view.setRootIndex(model.index(data['directory_path']))
                        
                elif form_type == 'tree':
                    # Si c'est un arbre d'objets (pour les réseaux par exemple)
                    tree_view = field['widget'].findChild(QTreeView)
                    if tree_view:
                        model = QStandardItemModel()
                        model.setHorizontalHeaderLabels(['alias'])
                    
                        # Ajouter les réseaux s'ils existent
                        if 'networks' in data:
                            for network in data['networks']:
                                niqsi = QStandardItem(network['alias' or 'name'])
                                model.appendRow(niqsi)
                        tree_view.setModel(model)
                            
                elif form_type == 'list-btn':
                    # Si c'est une liste de boutons
                    list_widget = field['widget'].findChild(QListWidget)
                    if list_widget:
                        list_widget.clear()
                        # Ajouter les éléments selon le contexte
                        if field['title'] == "Extensions Ouvert":
                            for ext in data.get('extensions', []):
                                list_widget.addItem(ext['name'])
                        elif field['title'] == "Network Object Ouvert":
                            # Ajouter les objets réseau ouverts
                            pass
                            
                # Mise à jour des actions si nécessaire
                if field.get('actions'):
                    for action in field['actions']:
                        if isinstance(action, dict) and action.get('callback') is None:
                            # Mettre à jour le callback avec le nouveau contexte
                            if action.get('tooltip') == 'Nouvelle Machine':
                                action['callback'] = lambda: self.create_new_machine(data)
                            elif action.get('tooltip') == 'Nouveau Réseau':
                                action['callback'] = lambda: self.create_new_network(data)
            
            # Émettre un signal pour informer de la mise à jour
            sdfsp.exchangeContext.emit({
                "action": "stack_updated",
                "index": index,
                "data": data
            })
            
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error updating stack widget: {str(e)}"
            )

    def initUI_menuBar(self):
        toolsBar = QToolBar(self)
        toolsBar.setMovable(False)
        toolsBar.setFloatable(False)

        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolsBar)

        names = ["&View", "&Settings"]

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
            
            if a.title in names[1]:
                spacer = QWidget()
                spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                toolsBar.addWidget(spacer)
                
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
                        if a.title in names:
                            toolsBar.addAction(e)
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
        """
        Change the current stacked widget and handle its visibility/size
        Args:
            index (int): Index of the stacked widget to show
        """
        current_index = self.primary_side_bar.currentIndex()
    
        if current_index == index:
            if self.h_splitter.sizes()[0] == 0:
                self.h_splitter.setSizes([220, self.h_splitter.width() - 220])
            else:
                self.h_splitter.setSizes([0, self.h_splitter.width()])
        elif current_index != index:
            if self.h_splitter.sizes()[0] == 0:
                # If sidebar is collapsed, expand it and change tab
                self.h_splitter.setSizes([220, self.h_splitter.width() - 220])
                self.primary_side_bar.setCurrentIndex(index)
            else:
                # Just change the tab
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
        try:
            # Lire le fichier de configuration
            a = FactoryConfFile(os.path.join(project.path, "lan_audacity.json"))
            a.read_file()

            # Créer une instance de LanAudacity avec les arguments requis
            rf = LanAudacity(directory_path=project.path,
                             directory_name=project.name)

            # Charger les données du fichier dans l'instance
            rf = rf.from_dict(a.file_data)

            # Ajouter le projet à la liste des projets actifs
            self.active_projects.append(rf)

            # Mettre à jour les widgets
            self.update_stackedWidget(0, rf.get_dict())
            self.update_stackedWidget(1, rf.get_dict())

        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading project: {str(e)}"
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
