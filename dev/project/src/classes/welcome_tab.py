from enum import Enum, auto
from typing import Optional, List, Dict
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os
import sys
import inspect


"""
    Objectif:
        - Créer une classe qui permet de créer un onglet avec des paramètres par défaut
        - Créer un onglet de bienvenue
    Remarque:
        Je compte bien comprendre comment fonctionne les classes "QTabWidget" et "QTabBar".
"""    

# class WelcomeTab(QWidget):
#     def __init__(self, parent: Optional[QWidget] = None) -> None:
#         super().__init__(parent)

#         self.initUI()
    
#     def initUI(self):
#         self.setLayout(QVBoxLayout(self))
#         self.layout().addStretch(1)
#         # TITRE
#         # SOUS-TITRE
#         # Qwidget->QHBox: Apps
#         # Box 1: Commencer
#         # Box 2: Récent
#         # Box 3: Custom
#         self.layout().addStretch(1)


class TabType(Enum):
    DEFAULT = auto()
    EDITOR = auto()
    NETWORK = auto()
    EXTENSION = auto()


class Tab(QWidget):
    """Base class for all tabs"""
    def __init__(self, parent=None, tab_type: TabType = None, title: str = ""):
        super().__init__(parent)
        self.tab_type = tab_type
        self.title = title
        self.modified = False
        
    def get_title(self) -> str:
        return f"{'*' if self.modified else ''}{self.title}"


class EditorTab(Tab):
    """Tab for file editing"""
    def __init__(self, parent=None, file_path: str = ""):
        super().__init__(parent, TabType.EDITOR, os.path.basename(file_path))
        self.file_path = file_path
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        self.editor = QPlainTextEdit(self)
        layout.addWidget(self.editor)
        
        # Load file content if exists
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    self.editor.setPlainText(f.read())
            except Exception as e:
                logging.error(f"Error loading file {self.file_path}: {str(e)}")
        
        # Connect signals
        self.editor.textChanged.connect(self.on_text_changed)
        
    def on_text_changed(self):
        if not self.modified:
            self.modified = True
            # Emit signal to update tab title
            if hasattr(self.parent(), 'update_tab_title'):
                self.parent().update_tab_title(self)


class NetworkObjectTab(Tab):
    """Tab for network objects like devices, interfaces etc."""
    def __init__(self, parent=None, object_data: Dict = None):
        title = object_data.get('name', 'Network Object')
        super().__init__(parent, TabType.NETWORK, title)
        self.object_data = object_data
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        # Add network object specific widgets here
        # This is a placeholder for the actual implementation
        layout.addWidget(QLabel(f"Network Object: {self.title}"))


class ExtensionTab(Tab):
    """Tab for extensions/plugins"""
    def __init__(self, parent=None, extension_data: Dict = None):
        title = extension_data.get('name', 'Extension')
        super().__init__(parent, TabType.EXTENSION, title)
        self.extension_data = extension_data
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        # Add extension specific widgets here
        # This is a placeholder for the actual implementation
        layout.addWidget(QLabel(f"Extension: {self.title}"))


class WelcomeTab(Tab):
    """Welcome tab shown by default when the application starts"""
    
    def __init__(self, parent=None):
        super().__init__(parent, TabType.DEFAULT, "Welcome")
        self.initUI()
        
    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(2, 2, 2, 2)

        # Add QScrollArea as main container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
                
    def get_tabs_by_type(self, tab_type: TabType) -> List[Tab]:
        """Get all tabs of a specific type"""
        return [
            self.widget(i) for i in range(self.count())
            if isinstance(self.widget(i), Tab) and self.widget(i).tab_type == tab_type
        ]