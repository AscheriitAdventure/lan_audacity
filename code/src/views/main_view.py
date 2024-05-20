from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import qtawesome as qta
from src.models.conf_file import ConfigurationFile
from src.models.worker import Worker
from src.models.lang_app import LanguageApp
from src.models.shortcut_app import ShortcutApp
from src.views.tabs_view import TabWidgetFactory
from src.views.general_tabs_view import GeneralTabsView, PreferencesTab, LogSignInTab
from src.views.explorer_view import (
    FilesExplorerWidget,
    NetExplorerWidget,
    SearchExplorerWidget,
    DLCExplorerWidget,
)
from main_app import current_dir
import logging


class MainView(QMainWindow):
    def __init__(self, software_manager: ConfigurationFile):
        super().__init__()
        self.softwareManager = software_manager
        self.langManager = LanguageApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['configuration_translate']['path']}"
            )
        )
        self.shortcut_manager = ShortcutApp(
            ConfigurationFile(
                f"{current_dir()}/{self.softwareManager.data['software']['configuration_key_shortcuts']['path']}"
            )
        )
        self.set_title()
        self.set_menu()
        # Central Object
        self.app_struct_window = QWidget(self)
        self.app_struct_window.setLayout(QVBoxLayout(self))
        self.setCentralWidget(self.app_struct_window)
        self.set_navbar()
        self.set_hwindow()
        # Status Bar
        self.prg_fnc_btn = QPushButton(self)
        self.spinner_animation = qta.Spin(self.prg_fnc_btn, autostart=False)
        icon = qta.icon('fa5s.circle-notch', color='RoyalBlue', animation=self.spinner_animation)
        self.prg_fnc_btn.setIcon(icon)
        self.statusBar().addPermanentWidget(self.prg_fnc_btn)
        self.prg_fnc_btn.hide()
    
    def runThreadFunc(self, method) -> None:
        self.prg_fnc_btn.show()
        # Démarrer l'animation de l'icône spinner
        self.start_spinner()
        # Utiliser QTimer pour démarrer le thread après un délai
        QTimer.singleShot(50, lambda: self.start_thread(method))
    
    def start_thread(self, method):
        self.thread = Worker(method)
        self.thread.finished.connect(self.stop_spinner)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
    
    def start_spinner(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_spinner)
        self.angle = 0
        self.timer.start(50)  # Déclencher toutes les 50 ms
    
    def stop_spinner(self):
        self.timer.stop()
        self.rotate_spinner(rotate=False)
    
    def rotate_spinner(self, rotate=True):
        if rotate:
            self.spinner_animation.start()
            self.prg_fnc_btn.show()
        else:
            self.spinner_animation.stop()
            self.prg_fnc_btn.hide()

    def set_navbar(self):
        # Navigation Bar
        self.nav_bar = QWidget(self)
        self.nav_bar.setLayout(QHBoxLayout(self))
        self.nav_bar.layout().setContentsMargins(0, 0, 0, 0)
        self.nav_bar.setFixedHeight(40)
        # Btn Home
        self.btn_home = QPushButton(qta.icon("fa5s.home"), "")
        self.btn_home.setToolTip(self.langManager.get_textTranslate("&Home"))
        self.btn_home.clicked.connect(self.toggle_home)
        self.nav_bar.layout().addWidget(self.btn_home)

        # Search Bar
        self.nav_bar.layout().addStretch()
        self.search_bar = QLineEdit(self.softwareManager.data["system"]["name"])
        self.search_bar.setFixedWidth(200)
        self.nav_bar.layout().addWidget(self.search_bar)

        # Language Btn
        self.nav_bar.layout().addStretch()
        self.btn_language = QPushButton(qta.icon("fa5s.language"), "")
        self.btn_language.setToolTip(self.langManager.get_textTranslate("Language"))
        self.nav_bar.layout().addWidget(self.btn_language)

        # Notification Btn
        self.btn_info = QPushButton(qta.icon("fa5s.bell", color="Orange"), "")
        self.btn_info.setToolTip(self.langManager.get_textTranslate("Notification"))
        self.nav_bar.layout().addWidget(self.btn_info)
        self.app_struct_window.layout().addWidget(self.nav_bar)

    def set_hwindow(self):
        # Horizontal Window
        self.hwindow = QWidget(self)
        self.hwindow.setLayout(QHBoxLayout(self))
        self.app_struct_window.layout().addWidget(self.hwindow)

        # Left Window
        self.toolbar_custom = QWidget(self)
        self.toolbar_custom.setLayout(QVBoxLayout(self))
        self.toolbar_custom.layout().setContentsMargins(0, 0, 0, 0)
        self.toolbar_custom.setFixedWidth(50)
        self.hwindow.layout().addWidget(self.toolbar_custom)
        self.set_toolbar()

        self.explore_cnt = QStackedWidget(self)
        self.explore_cnt.setMaximumWidth(250)
        self.explore_cnt.setAcceptDrops(True)
        self.explore_cnt.setContentsMargins(0, 0, 0, 0)
        self.hwindow.layout().addWidget(self.explore_cnt)

        # Central Window
        self.central_window = QSplitter(Qt.Vertical)
        self.hwindow.layout().addWidget(self.central_window)
        self.set_tab_widget()
        self.set_stack_widget()

    def set_toolbar(self):
        tool_item_lst = [
            {
                "icon": qta.icon("fa5s.project-diagram"),
                "text": self.langManager.get_textTranslate("Projects"),
                "action": self.toggle_projects,
            },
            {
                "icon": qta.icon("fa5s.copy"),
                "text": self.langManager.get_textTranslate("&Files"),
                "action": self.toggle_file_explorer,
            },
            {
                "icon": qta.icon("fa5s.search"),
                "text": self.langManager.get_textTranslate("Search..."),
                "action": self.toggle_search,
            },
            {
                "icon": qta.icon("fa5s.shapes"),
                "text": self.langManager.get_textTranslate("DLC"),
                "action": self.toggle_dlc,
            },
            {
                "icon": qta.icon("fa5s.user-circle"),
                "text": self.langManager.get_textTranslate("Log In"),
                "action": self.toggle_login,
            },
            {
                "icon": qta.icon("fa5s.cog"),
                "text": self.langManager.get_textTranslate("&Preferences"),
                "action": self.toggle_preferences,
            },
            {
                "icon": qta.icon("fa5s.sign-out-alt"),
                "text": self.langManager.get_textTranslate("&Exit"),
                "action": self.quit,
            },
        ]

        for item in tool_item_lst:
            if item["text"] == self.langManager.get_textTranslate("Log In"):
                self.toolbar_custom.layout().addStretch()
            btn = QPushButton(item["icon"], "")
            btn.setToolTip(item["text"])
            btn.clicked.connect(item["action"])
            self.toolbar_custom.layout().addWidget(btn)

    def set_stack_widget(self):
        # Explore Content Files
        self.files_tree = FilesExplorerWidget(
            self.langManager.get_textTranslate("&File"),
            current_dir(),
            self.edit_tab_widget,
            self.langManager,
        )
        self.explore_cnt.addWidget(self.files_tree)

        # Explore Content Projects
        self.projects_tree = NetExplorerWidget(
            self.langManager.get_textTranslate("Projects"),
            self.edit_tab_widget,
            self.langManager,
        )
        self.explore_cnt.addWidget(self.projects_tree)

        # Search Content
        self.search_tree = SearchExplorerWidget(
            self.langManager.get_textTranslate("Search"),
            self.edit_tab_widget,
            self.langManager,
        )
        self.explore_cnt.addWidget(self.search_tree)

        # Explore Content DLC
        self.dlc_tree = DLCExplorerWidget(
            self.langManager.get_textTranslate("DLC"),
            self.edit_tab_widget,
            self.langManager,
        )
        self.explore_cnt.addWidget(self.dlc_tree)

    def set_tab_widget(self):
        # Edit and Terminal Tab Widget
        self.edit_tab_widget = TabWidgetFactory(self)
        self.edit_tab_widget.currentChanged.connect(self.set_title)
        self.central_window.addWidget(self.edit_tab_widget)

        self.terminal_tab_widget = TabWidgetFactory(self)
        self.terminal_tab_widget.currentChanged.connect(self.set_title)
        self.central_window.addWidget(self.terminal_tab_widget)
        self.central_window.setSizes(
            [self.edit_tab_widget.height(), self.terminal_tab_widget.height()]
        )

    def set_menu(self):
        menu_bar_custom = self.menuBar()

        file_menu = menu_bar_custom.addMenu(self.langManager.get_textTranslate("&File"))
        view_menu = menu_bar_custom.addMenu(self.langManager.get_textTranslate("&View"))
        terminal_menu = menu_bar_custom.addMenu(
            self.langManager.get_textTranslate("&Terminal")
        )
        help_menu = menu_bar_custom.addMenu(self.langManager.get_textTranslate("&Help"))

        # File
        new_project = QAction(self.langManager.get_textTranslate("New Project"), self)
        new_project.setShortcut(self.shortcut_manager.get_shortcut("New Project"))
        new_project.triggered.connect(self.new_project)
        file_menu.addAction(new_project)

        new_network = QAction(self.langManager.get_textTranslate("New Network"), self)
        new_network.setShortcut(self.shortcut_manager.get_shortcut("New Network"))
        new_network.triggered.connect(self.new_device)
        file_menu.addAction(new_network)

        new_window = QAction(self.langManager.get_textTranslate("New Window"), self)
        new_window.setShortcut(self.shortcut_manager.get_shortcut("New Window"))
        new_window.triggered.connect(self.openNewWindow)
        file_menu.addAction(new_window)

        file_menu.addSeparator()

        open_project = QAction(self.langManager.get_textTranslate("Open Project"), self)
        file_menu.addAction(open_project)

        open_network = QAction(self.langManager.get_textTranslate("Open Network"), self)
        file_menu.addAction(open_network)

        save_project = QAction(self.langManager.get_textTranslate("Save"), self)
        save_project.setShortcut(self.shortcut_manager.get_shortcut("Save"))
        file_menu.addAction(save_project)

        save_as = QAction(self.langManager.get_textTranslate("Save as..."), self)
        save_as.setShortcut(self.shortcut_manager.get_shortcut("Save as..."))
        file_menu.addAction(save_as)

        export = QAction(self.langManager.get_textTranslate("Export"), self)
        export.setShortcut(self.shortcut_manager.get_shortcut("Export"))
        file_menu.addAction(export)

        export_as = QAction(self.langManager.get_textTranslate("Export as..."), self)
        export_as.setShortcut(self.shortcut_manager.get_shortcut("Export as..."))
        file_menu.addAction(export_as)

        file_menu.addSeparator()

        exit_action = QAction(self.langManager.get_textTranslate("&Exit"), self)
        exit_action.setShortcut(self.shortcut_manager.get_shortcut("&Exit"))
        exit_action.triggered.connect(self.quit)
        file_menu.addAction(exit_action)

        # View
        full_screen = QAction(self.langManager.get_textTranslate("Full Screen"), self)
        full_screen.setShortcut(self.shortcut_manager.get_shortcut("Full Screen"))
        full_screen.triggered.connect(self.full_screen)
        view_menu.addAction(full_screen)

        view_menu.addSeparator()

        show_toolbar = QAction(
            self.langManager.get_textTranslate("Show/Hide Toolbar"), self
        )
        show_toolbar.setCheckable(True)
        show_toolbar.setShortcut(
            self.shortcut_manager.get_shortcut("Show/Hide Toolbar")
        )
        show_toolbar.triggered.connect(self.show_hide_toolbar)
        view_menu.addAction(show_toolbar)

        show_terminal = QAction(
            self.langManager.get_textTranslate("Show/Hide Terminal"), self
        )
        show_terminal.setCheckable(True)
        show_terminal.setShortcut(
            self.shortcut_manager.get_shortcut("Show/Hide Terminal")
        )
        show_terminal.triggered.connect(self.show_hide_terminal)
        view_menu.addAction(show_terminal)

        # Terminal
        new_terminal = QAction(self.langManager.get_textTranslate("New Terminal"), self)
        new_terminal.setShortcut(self.shortcut_manager.get_shortcut("New Terminal"))
        new_terminal.triggered.connect(self.new_console)
        terminal_menu.addAction(new_terminal)

    def set_title(self, index=None):
        if index is None:
            title = self.softwareManager.data["system"]["name"]
        else:
            title = f"{self.softwareManager.data['system']['name']} - {index}"
        self.setWindowTitle(title)

    def quit(self):
        logging.info("The software has been closed.")
        self.close()

    def toggle_file_explorer(self):
        self.runThreadFunc(self.explore_cnt.setCurrentWidget(self.files_tree))

    def toggle_projects(self):
        logging.info("Projects")
        self.runThreadFunc(self.explore_cnt.setCurrentWidget(self.projects_tree))

    def new_project(self):
        logging.info("New Project")
        self.runThreadFunc(self.projects_tree.addNetwork())

    def new_device(self):
        logging.info("New Device")
        self.runThreadFunc(self.projects_tree.addDevice())

    def toggle_search(self):
        logging.info("Search")
        self.runThreadFunc(self.explore_cnt.setCurrentWidget(self.search_tree))

    def toggle_dlc(self):
        logging.info("DLC")
        self.runThreadFunc(self.explore_cnt.setCurrentWidget(self.dlc_tree))

    def toggle_home(self):
        logging.info("Home")
        self.runThreadFunc(self.edit_tab_widget.add_tab(GeneralTabsView(self.langManager, self), "Home"))

    def toggle_login(self):
        logging.info("Login")
        self.runThreadFunc(self.edit_tab_widget.add_tab(LogSignInTab(self.langManager), "Login"))

    def toggle_preferences(self):
        logging.info("Preferences")
        self.runThreadFunc(self.edit_tab_widget.add_tab(
            PreferencesTab(
                self.langManager, self.softwareManager, self
            ),
            "Preferences",
        ))

    def new_console(self):
        logging.info("New Console")
        self.runThreadFunc(self.terminal_tab_widget.add_tab(QWidget(self), "Console"))

    def full_screen(self):
        logging.info("Full Screen")
        self.runThreadFunc(self.showFullScreen())

    def show_hide_toolbar(self):
        logging.info("Show/Hide Toolbar")
        self.runThreadFunc(self.explore_cnt.setVisible(not self.explore_cnt.isVisible()))

    def show_hide_terminal(self):
        logging.info("Show/Hide Terminal")
        self.runThreadFunc(self.terminal_tab_widget.setVisible(not self.terminal_tab_widget.isVisible()))

    def openNewWindow(self):
        new_window = MainView(self.softwareManager)
        new_window.show()
        logging.info("New Window")
