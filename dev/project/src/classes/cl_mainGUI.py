from typing import Optional, ClassVar, Any, List
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect
import time
from dev.project.src.classes.cl_tab_2 import TabManager, Tab, WelcomeTab, EditorTab, NetworkObjectTab, ExtensionTab
from dev.project.src.classes.cl_stacked_objects import SDFSP
from dev.project.src.lib.template_tools_bar import *
from dev.project.src.classes.cl_dialog import DynFormDialog
from dev.project.src.classes.cl_lan_audacity import LanAudacity, Network
from dev.project.src.classes.cl_extented import IconApp, ProjectOpen
from dev.project.src.lib.qt_obj import newAction
from dev.project.src.lib.template_dialog import *
from dev.project.src.classes.cl_factory_conf_file import IconsManager, MenuBarManager, FactoryConfFile



class MainGUI(QMainWindow):

    processRunList: ClassVar[Signal] = Signal(list)

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)

        self.iconsManager = IconsManager(os.getenv("ICON_FILE_RSC"))
        self.menuBarManager = MenuBarManager(os.getenv("MENUBAR_FILE"))

        self.recent_projects: List[ProjectOpen] = [] # Liste des projets récents
        self.stackedWidgetList: List[SDFSP] = [] # Liste des widgets à empiler
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
        self.primary_center = TabManager(self)
        self.primary_center.setMinimumHeight(100)
        self.primary_center.tab_closed.connect(self.on_tab_closed)
        self.primary_center.tab_changed.connect(self.on_tab_changed)

        # Add welcome tab
        self.add_welcome_tab()

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
            sdfsp = SDFSP(debug=False, parent=self)

            # Connecter les signaux de double-clic
            sdfsp.itemDoubleClicked.connect(self.handle_item_double_click)

            for field in stack["fields"]:
                if "actions" in field and isinstance(field["actions"], list):
                    for action in field["actions"]:
                        if isinstance(action, dict):
                            callback = action.get("callback")
                            # Vérifier que callback est une chaîne de caractères
                            if isinstance(callback, str):
                                if callback_method := self.get_callback(callback):
                                    action["callback"] = callback_method
                                else:
                                    logging.warning(f"Callback '{callback}' not found")
                            elif callback is not None:
                                logging.warning(f"Invalid callback type: {type(callback)}")

            self.primary_side_bar.addWidget(sdfsp)
            self.stackedWidgetList.append(sdfsp)

            if self.active_projects != []:
                ao = self.active_projects[0]
                for field in stack["fields"]:
                    if field_form := field.get("form_list"):
                        if field_form == 'tree-file':
                            field["widget_data"] = ao.directory_path
                            field['title'] = ao.directory_name
                        elif field_form == 'tree':
                            field["widget_data"] = []
                        elif field_form == 'list-btn':
                            field["widget_data"] = []
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
                        field['widget'].setToolTip(f"Explorateur de Fichiers de {data['directory_name']}")
                        
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
                    if field['title']:
                        # Mettre à jour le titre avec le nom du projet
                        field['widget'].findChild(QLabel).setText(data['directory_name'].upper())
                        # Mettre à jour le tooltip
                        field['widget'].setToolTip(f"Explorateur de Réseaux de {data['directory_name']}")

                    tree_view = field['widget'].findChild(QTreeView)
                    if tree_view:
                        model = QStandardItemModel()
                        model.setHorizontalHeaderLabels(["alias","path"])
                        # Ajouter les réseaux s'ils existent
                        if 'networks' in data:
                            for network in data['networks']:
                                alias_item = QStandardItem(network["alias"])
                                path_item = QStandardItem(network["path"])
                                # Ajouter la ligne au modèle
                                model.appendRow([alias_item, path_item])
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

    ######## Native Function Operate on windows ########
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
    
    ######## class Method for stack functions #######
    def get_callback(self, callback_name: str):
        """
        Get the method reference for a callback name.
        
        Args:
            callback_name (str): Name of the callback method
            
        Returns:
            method: Reference to the method or None if not found
        """
        if hasattr(self, callback_name):
            return getattr(self, callback_name)
        logging.warning(f"{self.__class__.__name__}::get_callback: Callback {callback_name} not found")
        return None

    def refresh_tree_view(self) -> None:
        """
        Refresh all tree views (both file explorer and object trees) in the current stacked widget.
        Handles both QFileSystemModel and QStandardItemModel.
        """
        try:
            # Get the current stacked widget
            current_widget = self.primary_side_bar.currentWidget()
            if not current_widget or not hasattr(current_widget, 'active_fields'):
                return
                
            # Find all tree views in the current widget
            for field in current_widget.active_fields:
                if field.get('form_list') in ['tree-file', 'tree']:
                    tree_view = field['widget'].findChild(QTreeView)
                    if not tree_view:
                        continue
                        
                    # Get the current model
                    model = tree_view.model()
                    
                    if isinstance(model, QFileSystemModel):
                        # Refresh file system model
                        current_path = model.rootPath()
                        model.setRootPath("")  # Force refresh
                        model.setRootPath(current_path)
                    
                    elif isinstance(model, QStandardItemModel):
                        # For object trees, we need to reload the data
                        if self.active_projects:
                            project = self.active_projects[0]
                            # Reload data based on the field title/type
                            if field.get('title') == "Project Name":
                                # Refresh network tree
                                self.update_stackedWidget(
                                    self.primary_side_bar.currentIndex(), 
                                    project.get_dict()
                                )
                    
                    # Restore expanded state if needed
                    tree_view.repaint()
                    
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::refresh_tree_view: {str(e)}"
            )

    def collapse_all_tree_items(self) -> None:
        """
        Collapse all expanded items in both file explorer and object trees 
        in the current stacked widget.
        """
        try:
            # Get the current stacked widget
            current_widget = self.primary_side_bar.currentWidget()
            if not current_widget or not hasattr(current_widget, 'active_fields'):
                return
                
            # Find all tree views in the current widget
            for field in current_widget.active_fields:
                if field.get('form_list') in ['tree-file', 'tree']:
                    tree_view = field['widget'].findChild(QTreeView)
                    if tree_view:
                        # Collapse all items
                        tree_view.collapseAll()
                        
                        # For file system, ensure root is visible
                        model = tree_view.model()
                        if isinstance(model, QFileSystemModel):
                            root_index = model.index(model.rootPath())
                            tree_view.scrollTo(root_index)
                            tree_view.setExpanded(root_index, True)
                        
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::collapse_all_tree_items: {str(e)}"
            )

    def create_new_file(self, parent_path: str = None) -> None:
        """
        Create a new file via a dialog and refresh the file explorer.
        
        Args:
            parent_path (str, optional): Path where the new file should be created.
                                    If None, uses current directory.
        """
        try:
            # Create dialog for new file
            dialog = DynFormDialog(self, False)
            dialog.load_form(NEW_FILE)
            
            if dialog.exec_() == QDialog.DialogCode.Accepted:
                data = dialog.get_form_data()
                filename = data.get("filename")
                
                # Determine the full path
                if parent_path:
                    full_path = os.path.join(parent_path, filename)
                else:
                    if self.active_projects:
                        full_path = os.path.join(self.active_projects[0].directory_path, filename)
                    else:
                        full_path = os.path.join(os.getcwd(), filename)
                        
                # Check if file already exists
                if os.path.exists(full_path):
                    QMessageBox.warning(
                        self,
                        "Erreur",
                        f"Le fichier {filename} existe déjà!"
                    )
                    return
                    
                # Create the file
                try:
                    with open(full_path, 'w') as f:
                        f.write('')
                        
                    # Refresh the file explorer view
                    self.refresh_tree_view()
                        
                except IOError as e:
                    QMessageBox.critical(
                        self,
                        "Erreur",
                        f"Impossible de créer le fichier: {str(e)}"
                    )
                    
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::create_new_file: {str(e)}"
            )

    def create_new_folder(self, parent_path: str = None) -> None:
        """
        Create a new folder via a dialog and refresh the file explorer.
        
        Args:
            parent_path (str, optional): Path where the new folder should be created.
                                    If None, uses current directory.
        """
        try:
            # Create dialog for new folder
            dialog = DynFormDialog(self, False)
            dialog.load_form(NEW_FOLDER)
            
            if dialog.exec_() == QDialog.DialogCode.Accepted:
                data = dialog.get_form_data()
                foldername = data.get("foldername")
                
                # Determine the full path
                if parent_path:
                    full_path = os.path.join(parent_path, foldername)
                else:
                    if self.active_projects:
                        full_path = os.path.join(self.active_projects[0].directory_path, foldername)
                    else:
                        full_path = os.path.join(os.getcwd(), foldername)
                        
                # Check if folder already exists
                if os.path.exists(full_path):
                    QMessageBox.warning(
                        self,
                        "Erreur",
                        f"Le dossier {foldername} existe déjà!"
                    )
                    return
                    
                # Create the folder
                try:
                    os.makedirs(full_path)
                    
                    # Refresh the file explorer view
                    self.refresh_tree_view()
                        
                except OSError as e:
                    QMessageBox.critical(
                        self,
                        "Erreur",
                        f"Impossible de créer le dossier: {str(e)}"
                    )
                    
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {str(e)}"
            )
    
    def create_new_network(self) -> None:
        try:
            dialog = DynFormDialog(self, False)
            dialog.load_form(NEW_LAN)

            if dialog.exec_() == QDialog.DialogCode.Accepted:
                data = dialog.get_form_data()
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {data}"
                )
                # récupère le projet actif
                project = self.active_projects[0]
                new_lan = Network(name_object=data['network_name'], ospath=os.path.join(project.directory_path,"db","interfaces"))                
                # ajoute le réseau au projet
                project.add_network(new_lan.get_interface())
                project.update_lan_audacity()
                new_lan.dns_object = data.get('dns', None)
                new_lan.web_address.ipv4 = data.get('ipv4', None)
                new_lan.web_address.mask_ipv4 = data.get('mask_ipv4', None)
                new_lan.web_address.ipv6_local = data.get('ipv6', None)
                new_lan.web_address.check_data()

                self.update_stackedWidget(1, project.get_dict())

        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {str(e)}")

    def create_new_device(self, parent_path = None) -> None:
        try:
            dialog = DynFormDialog(self, False)
            dialog.load_form(NEW_UC)

            if dialog.exec_() == QDialog.DialogCode.Accepted:
                data = dialog.get_form_data()
                logging.debug(
                    f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {data}"
                )
                # récupère le projet actif
                project = self.active_projects[0]
                # récupère le réseau actif
                # crée un nouvel équipement
                # ajoute l'équipement au réseau
                # met à jour le projet
                # met à jour les widgets
                self.update_stackedWidget(1, project.get_dict())

        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {str(e)}")
    
    ######## class Method for tab functions ######
    def handle_item_double_click(self, item_data: dict):
        """
        Gère le double-clic sur un élément du TreeView.
        
        Args:
            item_data (dict): Données de l'élément cliqué avec les clés :
                - type: 'file' ou 'network'
                - path: chemin du fichier (pour type='file')
                - is_dir: booléen indiquant si c'est un dossier (pour type='file')
                - name: nom de l'objet (pour type='network')
                - id: identifiant de l'objet (pour type='network')
        """
        try:
            logging.info(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: {item_data}")
            if item_data['type'] == 'file' and not item_data['is_dir']:
                # Ouvre le fichier dans un éditeur
                self.open_file_in_editor(item_data['path'])
                
            elif item_data['type'] == 'network':
                # Ouvre l'objet réseau dans un nouvel onglet
                self.open_network_object(item_data)
                
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::handle_item_double_click: {str(e)}"
            )
    
    def open_file_in_editor(self, file_path: str) -> None:
        """Open a file in a new editor tab"""
        # Check if file is already open
        for tab in self.primary_center.get_tabs_by_type(Tab.TabType.EDITOR):
            if isinstance(tab, EditorTab) and tab.file_path == file_path:
                self.primary_center.setCurrentWidget(tab)
                return

        # Create new editor tab
        editor_tab = EditorTab(parent=self.primary_center, file_path=file_path)
        index = self.primary_center.add_tab(editor_tab)
        self.primary_center.setCurrentIndex(index)

        # Update "Editeur Ouvert" list
        self.update_open_tabs_list(Tab.TabType.EDITOR)

    def open_network_object(self, object_data: dict) -> None:
        """Open a network object in a new tab"""
        # Check if object is already open
        object_id = object_data.get('id')
        for tab in self.primary_center.get_tabs_by_type(Tab.TabType.NETWORK):
            if isinstance(tab, NetworkObjectTab) and tab.object_data.get('id') == object_id:
                self.primary_center.setCurrentWidget(tab)
                return

        # Create new network object tab
        network_tab = NetworkObjectTab(object_data=object_data, parent=self.primary_center)
        index = self.primary_center.add_tab(network_tab)
        self.primary_center.setCurrentIndex(index)

        # Update "Network Object Ouvert" list
        self.update_open_tabs_list(Tab.TabType.NETWORK)

    def open_extension(self, extension_data: dict) -> None:
        """Open an extension in a new tab"""
        # Check if extension is already open
        ext_id = extension_data.get('id')
        for tab in self.primary_center.get_tabs_by_type(Tab.TabType.EXTENSION):
            if isinstance(tab, ExtensionTab) and tab.extension_data.get('id') == ext_id:
                self.primary_center.setCurrentWidget(tab)
                return

        # Create new extension tab
        extension_tab = ExtensionTab(parent=self.primary_center, extension_data=extension_data)
        index = self.primary_center.add_tab(extension_tab)
        self.primary_center.setCurrentIndex(index)

        # Update "Extensions Ouvert" list
        self.update_open_tabs_list(Tab.TabType.EXTENSION)

    def update_open_tabs_list(self, tab_type: Tab.TabType) -> None:
        """Update the corresponding open tabs list based on tab type"""
        tabs = self.primary_center.get_tabs_by_type(tab_type)
        tab_titles = [tab.title for tab in tabs]

        # Find the correct list widget based on tab type
        list_widget = None
        field_title = None

        if tab_type == Tab.TabType.EDITOR:
            field_title = "Editeur Ouvert"
        elif tab_type == Tab.TabType.NETWORK:
            field_title = "Network Object Ouvert"
        elif tab_type == Tab.TabType.EXTENSION:
            field_title = "Extensions Ouvert"

        # Update the corresponding list widget
        for stack_widget in self.stackedWidgetList:
            for field in stack_widget.active_fields:
                if field.get('title') == field_title:
                    list_widget = field['widget'].findChild(QListWidget)
                    if list_widget:
                        list_widget.clear()
                        list_widget.addItems(tab_titles)
                    break

    def on_tab_closed(self, tab: Tab) -> None:
        """Handle tab closure"""
        self.update_open_tabs_list(tab.tab_type)

    def on_tab_changed(self, tab: Tab) -> None:
        """Handle tab change"""
        # Update UI elements based on the type of tab that's now active
        pass  # Implement based on specific requirements

    def add_welcome_tab(self) -> None:
        """Add the welcome tab to the primary center"""
        welcome_tab = WelcomeTab(self.primary_center)
        welcome_tab.update_recent_projects(self.recent_projects)
        self.primary_center.add_tab(welcome_tab)
    
    def update_welcome_tab(self) -> None:
        """Update the welcome tab with current data"""
        for i in range(self.primary_center.count()):
            tab = self.primary_center.widget(i)
            if isinstance(tab, WelcomeTab):
                tab.update_recent_projects(self.recent_projects)
                break
    
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
