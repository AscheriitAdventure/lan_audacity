from enum import Enum, auto
from typing import Union, List, Dict, ClassVar, Optional
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect
from pathlib import Path

from dev.project.src.classes.cl_clicontext import CLIconText, CLWIT
from dev.project.src.classes.cl_extented import IconApp
from dev.project.src.classes.cl_stacked_objects_2 import SDFOT, SDFSP
from dev.project.src.lib.template_tools_bar import DEVICE_TAB, NETWORK_TAB, DEFAULT_SIDE_PANEL
from dev.project.src.view.components.cl_codeEditor_2 import CodeEditor
from dev.project.src.view.components.cl_breadcrumbs_2 import QBreadcrumbs


class Tab(QWidget):
    class TabType(Enum):
        DEFAULT = auto()
        EDITOR = auto()
        NETWORK = auto()
        EXTENSION = auto()

    """Base class for all tabs"""

    def __init__(self, parent=None, tab_type: TabType = None, title: str = ""):
        super().__init__(parent)
        self.tab_type = tab_type
        self.title = title
        self.modified = False

    def get_title(self) -> str:
        return f"{'*' if self.modified else ''}{self.title}"


class TabManager(QTabWidget):
    """Enhanced tab widget with additional management features"""

    tab_closed = Signal(Tab)  # Emitted when a tab is closed
    tab_changed = Signal(Tab)  # Emitted when active tab changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        # Connect signals
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.on_current_changed)

    def add_tab(self, tab: Tab) -> int:
        """Add a new tab and return its index"""
        index = self.addTab(tab, tab.get_title())
        return index

    def close_tab(self, index: int) -> None:
        """Handle tab closing with confirmation if needed"""
        tab = self.widget(index)
        if isinstance(tab, Tab):
            if tab.modified:
                reply = QMessageBox.question(
                    self,
                    'Save Changes?',
                    f'Do you want to save changes to {tab.title}?',
                    QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
                )

                if reply == QMessageBox.StandardButton.Save:
                    # Handle saving
                    pass
                elif reply == QMessageBox.StandardButton.Cancel:
                    return

            self.removeTab(index)
            self.tab_closed.emit(tab)

    def update_tab_title(self, tab: Tab) -> None:
        """Update the title of a tab"""
        index = self.indexOf(tab)
        if index >= 0:
            self.setTabText(index, tab.get_title())

    def on_current_changed(self, index: int) -> None:
        """Handle tab selection change"""
        if index >= 0:
            tab = self.widget(index)
            if isinstance(tab, Tab):
                self.tab_changed.emit(tab)

    def get_tabs_by_type(self, tab_type: Tab.TabType) -> List[Tab]:
        """Get all tabs of a specific type"""
        return [
            self.widget(i) for i in range(self.count())
            if isinstance(self.widget(i), Tab) and self.widget(i).tab_type == tab_type
        ]


class WelcomeTab(Tab):
    """Welcome tab shown by default when the application starts"""

    def __init__(self, parent=None):
        super().__init__(parent, Tab.TabType.DEFAULT, "Welcome")
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(2, 2, 2, 2)

        # Add QScrollArea as main container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Create container widget for scroll area
        container = QWidget()
        scroll_layout = QVBoxLayout(container)
        scroll_layout.setSpacing(2)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Add scroll area to main layout
        main_layout.addWidget(scroll)
        scroll.setWidget(container)

        # Use scroll_layout instead of main_layout for content
        main_layout = scroll_layout

        # Header section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)

        title = QLabel("Welcome to LAN Audacity")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Get started with your network management")
        subtitle.setStyleSheet("font-size: 16px; color: #666;")

        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Actions section
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setSpacing(20)

        # Start box
        start_box = self._create_action_box(
            "Get Started",
            [
                ("New Project", "mdi6.folder-plus-outline", "new_project"),
                ("Open Project", "mdi6.folder-open-outline", "open_folder_project"),
                ("Import Project", "mdi6.folder-download-outline", None)
            ]
        )

        # Recent box
        recent_box = self._create_action_box(
            "Recent Projects",
            [("No recent projects", "", None)],
            fixed_height=200
        )

        # Help box
        help_box = self._create_action_box(
            "Help & Resources",
            [
                ("Documentation", "mdi6.book-open-page-variant-outline", None),
                ("Tutorial", "mdi6.school-outline", None),
                ("About", "mdi6.information-outline", None)
            ]
        )

        actions_layout.addWidget(start_box)
        actions_layout.addWidget(recent_box)
        actions_layout.addWidget(help_box)

        # Add all sections to main layout
        main_layout.addWidget(header_widget)
        main_layout.addWidget(actions_widget)
        main_layout.addStretch()

    def _create_action_box(self, title: str, actions: list, fixed_height: int = None) -> QGroupBox:
        """Create a grouped box of actions

        Args:
            title (str): Box title
            actions (list): List of tuples (label, icon_name, callback_name)
            fixed_height (int, optional): Fixed height for the box
        """
        box = QGroupBox(title)
        box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        if fixed_height:
            box.setFixedHeight(fixed_height)

        layout = QVBoxLayout(box)
        layout.setSpacing(10)

        for label, icon_name, callback_name in actions:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px;
                    border: none;
                    background: transparent;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                    border-radius: 4px;
                }
            """)

            if icon_name:
                from qtawesome import icon
                btn.setIcon(icon(icon_name))

            if callback_name and hasattr(self.parent(), callback_name):
                btn.clicked.connect(getattr(self.parent(), callback_name))
            elif not callback_name:
                btn.setEnabled(False)

            layout.addWidget(btn)

        layout.addStretch()
        return box

    def update_recent_projects(self, recent_projects: list) -> None:
        """Update the recent projects list

        Args:
            recent_projects (list): List of recent project objects
        """
        recent_box = self.findChild(QGroupBox, "Recent Projects")
        if recent_box:
            # Clear existing buttons
            while recent_box.layout().count() > 0:
                item = recent_box.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # Add new project buttons
            if recent_projects:
                for project in recent_projects:
                    btn = QPushButton(project.name)
                    btn.setStyleSheet("""
                        QPushButton {
                            text-align: left;
                            padding: 8px;
                            border: none;
                            background: transparent;
                        }
                        QPushButton:hover {
                            background: #f0f0f0;
                            border-radius: 4px;
                        }
                    """)
                    btn.clicked.connect(
                        lambda checked, p=project: self.parent().open_recent_project(p)
                    )
                    recent_box.layout().addWidget(btn)
            else:
                label = QLabel("No recent projects")
                label.setStyleSheet("color: #666; padding: 8px;")
                recent_box.layout().addWidget(label)

            recent_box.layout().addStretch()


class EditorTab(Tab):

    cursorLocationChanged: ClassVar[Signal] = Signal(int, int)

    def __init__(self, file_path: str = "", debug: bool = False, parent=None):
        super().__init__(parent, Tab.TabType.EDITOR, os.path.basename(
            file_path) if file_path else "Untitled")
        self.file_path = ""
        self.debug = debug
        self.functionBtnList: List[QPushButton] = []

        self.setFilePath(file_path)
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Breadcrumbs
        self.breadcrumbs = QBreadcrumbs(
            self._generatedBtnList(), self.debug, self)
        layout.addWidget(self.breadcrumbs, 0, 0, 1, 1)
        # Actions (Save, Read[On/Off])
        self.actions = QWidget()
        layout.addWidget(self.actions, 0, 2, 1, 1)
        # Code Editor
        self.editor = CodeEditor(parent=self)
        self.editor.addAreaActions(CodeEditor.ActionArea.LineNumber)
        layout.addWidget(self.editor, 1, 0, 1, 3)

        self._loadText()

        # Connect signals
        self.editor.textChanged.connect(self.onTextChanged)

    def setFilePath(self, file_path: str):
        if os.path.exists(file_path):
            self.file_path = Path(os.path.normpath(file_path))
        else:
            self.file_path = ""
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Le fichier n'existe pas")

    def _generatedBtnList(self) -> List[QPushButton]:
        btnList = []
        objPathList = self.file_path.parts
        for i in range(len(objPathList)):
            btn = QPushButton(objPathList[i])
            fontMetrics = QFontMetrics(btn.font())
            btn.setFlat(True)
            btn.setMaximumWidth(fontMetrics.horizontalAdvance(btn.text())+10)
            # Ajoute un tooltip indiquant le chemin absolu
            absPath = os.path.abspath(os.sep.join(objPathList[:i+1]))
            btn.setToolTip(absPath)
            # Ajoute à la liste des boutons
            btnList.append(btn)
        return btnList

    def onTextChanged(self):
        if not self.modified:
            self.modified = True
            if hasattr(self.parent(), "update_tab_title"):
                self.parent().update_tab_title(self)

    def _loadText(self):
        try:
            with open(self.file_path, 'r') as f:
                self.editor.setText(f.read())
        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading file {self.file_path}: {str(e)}")

    def addFuncBtn(self, btns: Union[QPushButton, List[QPushButton]]):
        if isinstance(btns, list):
            for btn in btns:
                self.functionBtnList.append(btn)
        else:
            self.functionBtnList.append(btns)


class NetworkObjectTab(Tab):
    class DomainType(Enum):
        DEVICE = auto() # Objet créer à partir d'un device brut
        INTERFACE = auto() # Objet créer à partir d'une box FAI
        VLAN = auto() # Objet créer à partir d'un device
        OTHER = auto() # Objet créer à partir de qqch

    """Tab for network objects like devices, interfaces etc."""

    def __init__(self, object_data: Optional[Dict] = None, parent=None):
        super().__init__(parent, Tab.TabType.NETWORK, object_data.get('name', 'Network Object'))
        self.rootData = object_data
        self.stackedWidgetList: List[QWidget] = []
        self.domainType: NetworkObjectTab.DomainType = self.DomainType.OTHER

        self.initUI()
        self._loadData()

    def initUI(self):
        # Main layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Add Scroll Area
        self._loadScrollArea()

        # Add Object 1 --> Custom List Widget Icon Text
        self._zone1 = QWidget()
        self._zone1Layout = QVBoxLayout(self._zone1)
        self._zone1Layout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.addWidget(self._zone1, 0, 0, 1, 1)
        
        # Add Object 2 --> Stacked 
        self._zone2 = QStackedWidget(self)
        self._zone2.setMinimumWidth(100)
        self.scrollLayout.addWidget(self._zone2, 0, 1, 1, 1, Qt.AlignmentFlag.AlignTop)

    def _loadScrollArea(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainLayout.addWidget(self.scrollArea)

        # Create container widget for scroll area
        self.scrollContainer = QWidget()
        self.scrollArea.setWidget(self.scrollContainer)
        self.scrollLayout = QGridLayout(self.scrollContainer)

    def _loadData(self):
        # Définir quel stack utilisé pour l'affichage
        domain_type = os.path.basename(os.path.dirname(self.rootData['path']))
        logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Domain type: {domain_type}")

        if domain_type == 'interfaces':
            self.domainType = self.DomainType.INTERFACE
            self._loadStackData(NETWORK_TAB)
        elif domain_type == 'desktop':
            self.domainType = self.DomainType.DEVICE
            self._loadStackData(DEVICE_TAB)
        else:
            self.domainType = self.DomainType.OTHER
            self._loadStackData(DEFAULT_SIDE_PANEL)
    
    def _loadStackData(self, data: Dict):
        sdfsp = SDFOT(debug=False, parent=self)

        btn_list: List[QPushButton] = []

        for f in data.get("fields", []):
            btn = QPushButton()
            btn.setText(f.get("title", ""))
            btn.setToolTip(f.get("tooltip", ""))
            if icon := f.get("icon"):
                ico = IconApp.from_dict(icon)
                btn.setIcon(ico.get_qIcon())
            btn.setFlat(True)
            # btn.clicked.connect(lambda checked, f=f: self.updateStackedWidget(0, f))
            btn_list.append(btn)

            # if "actions" in f and isinstance(f["actions"], list):
            #     for a in f["actions"]:
            #         if isinstance(a, dict) and "callback" in a and a["callback"] is not None:
            #             cbk = a.get("callback")
            #             if isinstance(cbk, str):
            #                 if cbk_method := self.get_callback(cbk):
            #                     a["callback"] = cbk_method
            #                 else:
            #                     logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Callback method {cbk} not found")
            #             elif cbk is not None:
            #                 logging.warning(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Invalid callback type: {type(cbk)}")
        
            # self._zone2.addWidget(sdfsp)
            # self.stackedWidgetList.append(sdfsp)
        
            # sdfsp.initDisplay(f)
        
        logging.debug(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Button list: {btn_list}")
        params = {
            "toggle": True, 
            "search": False,
            "parent": self
        }

        if len(btn_list) > 0:
            o = CLWIT(**params)
            for b in btn_list:
                o.add_btn(b)
            self._zone1Layout.addWidget(o)

    def updateStackedWidget(self, index: int, data: Dict):
        """
            Met à jour les données d'un widget et de ses fields
            Args:
                index (int): Index du widget à mettre à jour
                data (dict): Données à mettre à jour
        """
        try:
            sdfsp: SDFOT = self.stackedWidgetList[index]

            for f in sdfsp.activeFields:
                form_type = f.get("form_list")

                if form_type == "fmcg": # Fixed Mosaics Cards Grid
                    pass
                elif form_type == "dmcg": # Dynamic Mosaics Cards Grid
                    pass
                else: # Default Ressource Form
                    pass

                if f.get('actions'):
                    for a in f['actions']:
                        if isinstance(a, dict) and a.get('callback') is None:
                            if a.get('tooltip') == 'update':
                                a['callback'] = self.updateStackedWidget
                
            sdfsp.exchangeContext.emit({
                "action": "stack_updated",
                "index": index,
                "data": data
            })

        except Exception as e:
            logging.error(
                f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error updating stack widget: {str(e)}"
            )

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
    
    def handleItemSimpleClick(self, data: Dict):
        """
        Gère le clic sur un élément du CLWIT.
        
        Args:
            item_data (dict): Données de l'élément cliqué avec les clés :
                - name: nom de l'objet 
                - id: identifiant de l'objet 
        """
        pass


class ExtensionTab(Tab):
    """Tab for extensions/plugins"""

    def __init__(self, parent=None, extension_data: Dict = None):
        title = extension_data.get('name', 'Extension')
        super().__init__(parent, Tab.TabType.EXTENSION, title)
        self.extension_data = extension_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Add extension specific widgets here
        # This is a placeholder for the actual implementation
        layout.addWidget(QLabel(f"Extension: {self.title}"))
