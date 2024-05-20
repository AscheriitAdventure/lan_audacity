import sys
import qdarkstyle
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from _src._mdl.mdl_managers import SettingsModel, TextTranslateManager
from _src._mdl.mdl_itm import Device, NetworkManager
from _src._vues.card_vues import Card
from _src._vues.tree_vues import TreeviewDefault
from _src._vues.settings_vues import SettingsMenu


class DeviceViewInfo(QWidget):
    def __init__(self, obj_manager: SettingsModel, txt_manager: TextTranslateManager,
                 device_item: Device | None = None, parent=None):
        super().__init__(parent)
        self.txtTranslate = txt_manager
        self.objManager = obj_manager
        self.device = device_item
        self.set_ui()

    def set_ui(self):
        # Création d'un layout grid pour organiser les cartes
        grid_layout = QGridLayout()
        widget_layout = QWidget()  # Création d'un widget pour encapsuler le grid layout
        widget_layout.setLayout(grid_layout)

        # Objets
        item_link = [
            {
                'label': 'Network Info',
                'card_list': [
                    {
                        'title': 'H',
                        'corps_card': 'e'
                    },
                    {
                        'title': 'll',
                        'corps_card': 'o'
                    },
                    {
                        'title': 'W',
                        'corps_card': 'o'
                    },
                ]
            },
            {
                'label': 'Network Info',
                'card_list': [
                    {
                        'title': 'H',
                        'corps_card': 'e'
                    },
                    {
                        'title': 'll',
                        'corps_card': 'o'
                    },
                    {
                        'title': 'W',
                        'corps_card': 'o'
                    },
                ]
            },
        ]
        key_x: int = 0
        for item in item_link:
            lbl_titre = QLabel(item['label'])
            grid_layout.addWidget(lbl_titre, key_x, 0, 1, 5)
            key_y: int = 0
            for card in item['card_list']:
                # Création de plusieurs cartes et ajout dans le grid layout
                card_item = Card(title=QLabel(card['title']), corps_card=QTextEdit(card['corps_card']))
                grid_layout.addWidget(card_item, key_x+1, key_y, 1, 1)
                key_y += 1
            key_x += 2

        # Création de la zone de défilement et ajout du widget à l'intérieur
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permet à la zone de défilement de s'adapter à la taille du contenu
        scroll_area.setWidget(widget_layout)  # Ajout du widget contenant le grid layout

        # Ajout de la zone de défilement à la disposition principale du widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Activation de la possibilité de drag and drop
        self.setAcceptDrops(True)


class DeviceViewMenu(QWidget):
    def __init__(self, obj_manager: SettingsModel, txt_manager: TextTranslateManager,
                 device_item: Device | None = None, parent=None):
        super().__init__(parent)
        self.textTranslate = txt_manager
        self.device = device_item
        self.objManager = obj_manager

        self.set_ui()

    def set_ui(self):
        deviceLayout = QGridLayout(self)
        obj_menu_vbar = QVBoxLayout(self)
        obj_menu_vbar.setContentsMargins(0, 0, 0, 0)
        obj_menu_vbar_container = QWidget(self)
        obj_menu_vbar_container.setLayout(obj_menu_vbar)
        deviceLayout.addWidget(obj_menu_vbar_container, 0, 0, 5, 1,
                               Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setLayout(deviceLayout)

        # Extend btn
        self.extd_name = self.textTranslate.get_txt('Extends').textTranslate
        self.extend_btn = QPushButton(self.objManager.get_1_icon('extend_icon').objIcon, self.extd_name, self)
        self.extend_btn.setCheckable(True)
        self.extend_btn.icon().pixmap(48, 48)
        self.extend_btn.setToolTip(self.extd_name)
        obj_menu_vbar.addWidget(self.extend_btn)

        # Device Info btn
        self.info_name = self.textTranslate.get_txt('Info Device').textTranslate
        self.info_btn = QPushButton(self.objManager.get_1_icon('info_device').objIcon, self.info_name, self)
        self.info_btn.setToolTip(self.info_name)
        obj_menu_vbar.addWidget(self.info_btn)
        # Device net map btn
        self.map_name = self.textTranslate.get_txt('Map Device').textTranslate
        self.map_btn = QPushButton(self.objManager.get_1_icon('map_device').objIcon, self.map_name, self)
        self.map_btn.setToolTip(self.map_name)
        obj_menu_vbar.addWidget(self.map_btn)
        # Device Possibility
        ## Affiche autant de btn que de fonction disponible pour ce type de device
        ## Exemple: type = printer -> affiche le niveau d'encre
        ## Exemple: type = routeur/switch -> affiche la carte réseau à partir de la table de routage
        ## Exemple: type = routeur/switch L2/L3 -> affiche les vlans
        ## Exemple: type = hub/routeur/switch -> affiche les ports et leurs liens (si possible paramètrage)

        # Stacked layout pour gérer les vues changeantes
        self.stacked_layout = QStackedLayout()
        deviceLayout.addLayout(self.stacked_layout, 1, 1, 5, 1, Qt.AlignmentFlag.AlignTop)

        # Connecter les signaux aux slots pour afficher les différentes vues
        self.extend_btn.clicked.connect(self.toggle_btns)
        self.info_btn.clicked.connect(self.view_info)

        # Créer les vues pour chaque menu
        self.info_menu = DeviceViewInfo(self, self.objManager, self.textTranslate)
        self.stacked_layout.addWidget(self.info_menu)

    def toggle_btns(self):
        if self.extend_btn.isChecked():
            self.extend_btn.setText('')
            self.info_btn.setText('')
            self.map_btn.setText('')
        else:
            self.extend_btn.setText(self.extd_name)
            self.info_btn.setText(self.info_name)
            self.map_btn.setText(self.map_name)

    def view_info(self):
        self.stacked_layout.setCurrentWidget(self.info_menu)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settingsManager = SettingsModel()
        self.textTranslate = TextTranslateManager()
        self.deviceManager = NetworkManager()
        self.textTranslate.languageChoice = 'Français'
        self.title = "Lan Audacity"
        self.set_title()
        self.window_icon = self.settingsManager.get_1_icon('window_icon').objIcon
        self.setWindowIcon(self.window_icon)
        self.setGeometry(100, 100, 500, 300)

        # Le lieu d'action de toutes mes fonctionnalités
        self.centerTabEdit = QTabWidget(self, movable=True, tabsClosable=True)
        self.centerTabEdit.tabCloseRequested.connect(self.closeTabEdit)
        self.centerTabEdit.currentChanged.connect(self.set_title)

        # Création du widget de terminal
        self.terminal = QTabWidget(self, movable=True, tabsClosable=True)
        self.terminal.tabCloseRequested.connect(self.closeTabTerminal)

        # Création du QTreeView
        self.tree_view = TreeviewDefault(self.deviceManager, self.settingsManager, self.textTranslate)

        # Création du splitter vertical
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.centerTabEdit)
        self.splitter.addWidget(self.terminal)

        # Création du splitter horizontal
        self.splitter_horizontal = QSplitter(Qt.Horizontal)
        self.splitter_horizontal.addWidget(self.tree_view)
        self.splitter_horizontal.addWidget(self.splitter)

        # Ajout du splitter comme widget central
        self.setCentralWidget(self.splitter_horizontal)

        # Définir la largeur minimale du QTreeView
        self.tree_view.setMinimumWidth(200)
        self.tree_view.setMaximumWidth(250)

        # Ajuster les tailles des widgets enfants du QSplitter horizontal
        self.splitter_horizontal.setSizes([self.tree_view.sizeHint().width(), self.splitter.sizeHint().width()])

        self.set_menuBar()

    def set_menuBar(self):
        # Menu barre
        menu_bar = self.menuBar()

        file_bar = menu_bar.addMenu(self.textTranslate.get_txt('&File').textTranslate)
        edit_bar = menu_bar.addMenu(self.textTranslate.get_txt('&Edit').textTranslate)
        view_bar = menu_bar.addMenu(self.textTranslate.get_txt('&View').textTranslate)
        terminal_bar = menu_bar.addMenu(self.textTranslate.get_txt('&Terminal').textTranslate)
        settings_bar = menu_bar.addMenu(self.textTranslate.get_txt('&Settings').textTranslate)
        help_bar = menu_bar.addMenu(self.textTranslate.get_txt('&Help').textTranslate)

        open_tree_netscan_action = QAction(self.settingsManager.get_1_icon('netscan_icon').objIcon,
                                           self.textTranslate.get_txt(
                                               self.settingsManager.get_1_keyboard('New Scan').nameAction)
                                           .textTranslate,
                                           self)
        open_tree_netscan_action.setStatusTip(
            self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('New Scan').nameAction).textTranslate)
        open_tree_netscan_action.setShortcut(self.settingsManager.get_1_keyboard('New Scan').keyShortcut)
        file_bar.addAction(open_tree_netscan_action)
        file_bar.addSeparator()

        exit_action = QAction(self.settingsManager.get_1_icon('exit_icon').objIcon,
                              self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('&Exit').nameAction).textTranslate,
                              self)
        exit_action.setStatusTip(self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('&Exit').nameAction).textTranslate)
        exit_action.setShortcut(self.settingsManager.get_1_keyboard('&Exit').keyShortcut)
        exit_action.triggered.connect(self.quit)
        file_bar.addAction(exit_action)

        open_tab_home_action = QAction(self.settingsManager.get_1_icon('window_icon').objIcon,
                                       self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Home').nameAction).textTranslate,
                                       self)
        open_tab_home_action.setShortcut(self.settingsManager.get_1_keyboard('Home').keyShortcut)
        open_tab_home_action.setStatusTip(self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Home').nameAction).textTranslate)
        open_tab_home_action.triggered.connect(self.openHome)
        settings_bar.addAction(open_tab_home_action)

        open_tab_settings_action = QAction(self.settingsManager.get_1_icon('settings_icon').objIcon,
                                           self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Params').nameAction).textTranslate,
                                           self)
        open_tab_settings_action.setShortcut(self.settingsManager.get_1_keyboard('Params').keyShortcut)
        open_tab_settings_action.setStatusTip(self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Params').nameAction).textTranslate)
        open_tab_settings_action.triggered.connect(self.openParams)
        settings_bar.addAction(open_tab_settings_action)

        show_terminal_action = QAction(self.settingsManager.get_1_icon('console_icon').objIcon,
                                       self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('New Terminal').nameAction).textTranslate,
                                       self)
        show_terminal_action.setShortcut(self.settingsManager.get_1_keyboard('New Terminal').keyShortcut)
        show_terminal_action.setStatusTip(self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('New Terminal').nameAction).textTranslate)
        show_terminal_action.triggered.connect(self.showTerminal)
        terminal_bar.addAction(show_terminal_action)

        hide_terminal_action = QAction(self.settingsManager.get_1_icon('hide_console_icon').objIcon,
                                       self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Hide Terminal').nameAction).textTranslate,
                                       self)
        hide_terminal_action.setShortcut(self.settingsManager.get_1_keyboard('Hide Terminal').keyShortcut)
        hide_terminal_action.setStatusTip(self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Hide Terminal').nameAction).textTranslate)
        hide_terminal_action.triggered.connect(self.hideTerminal)
        view_bar.addAction(hide_terminal_action)

        # Création d'un QAction pour masquer/afficher le QTreeView
        self.toggle_tree_view_action = QAction(self.textTranslate.get_txt(self.settingsManager.get_1_keyboard('Show Tree View').nameAction).textTranslate, self)
        self.toggle_tree_view_action.setShortcut(self.settingsManager.get_1_keyboard('Show Tree View').keyShortcut)
        self.toggle_tree_view_action.setCheckable(True)
        self.toggle_tree_view_action.setChecked(True)
        self.toggle_tree_view_action.triggered.connect(self.toggleTreeView)

        # Ajout du QAction à la barre de menus
        view_bar.addAction(self.toggle_tree_view_action)

        # Définir la visibilité initiale du QTreeView
        self.tree_view.setVisible(True)

        # Ajout de la barre d'état
        self.statusBar().showMessage('Ready', 5000)
        self.hideTerminal()

    def quit(self):
        self.destroy()

    def set_title(self, index=None):
        if index is None:
            title = "Lan Audacity"
        else:
            title = f"Lan Audacity - {self.centerTabEdit.tabText(index)}"
        self.setWindowTitle(title)

    def openTabObjTree(self, index):
        # Récupérer l'item sélectionné dans le QTreeView
        item = self.tree_view.netTreeModel.itemFromIndex(index)

        # Vérifier si un onglet avec le même nom existe déjà
        existing_tab = self.findChild(QWidget, item.text())
        if existing_tab:
            # Si l'onglet existe déjà, le sélectionner
            self.centerTabEdit.setCurrentWidget(existing_tab)
        else:
            # Déterminer si l'élément sélectionné est un parent ou un enfant
            if item.parent():
                print("Enfant sélectionné:", item.text())
                # Sinon, créer un nouvel onglet
                tab = DeviceViewMenu(self.settingsManager, self.textTranslate)
            else:
                print("Parent sélectionné:", item.text())
                # Sinon, créer un nouvel onglet
                tab = DeviceViewMenu(self.settingsManager, self.textTranslate)
            tab.setObjectName(item.text())

            # Ajouter l'onglet à centerTabEdit
            self.centerTabEdit.addTab(tab, item.text())

    # Méthode pour fermer un onglet
    def closeTabTerminal(self, index):
        self.terminal.removeTab(index)

    def closeTabEdit(self, index):
        self.centerTabEdit.removeTab(index)

    def toggleTreeView(self):
        self.tree_view.setVisible(not self.tree_view.isVisible())
        self.toggle_tree_view_action.setChecked(self.tree_view.isVisible())
        self.splitter_horizontal.setSizes(
            [self.tree_view.sizeHint().width() if self.tree_view.isVisible() else 0, self.splitter.sizeHint().width()])

    def openParams(self):
        page = SettingsMenu(self.settingsManager, self.textTranslate, self.centerTabEdit)
        self.centerTabEdit.addTab(page, self.textTranslate.get_txt('Settings').textTranslate)

    def openHome(self):
        page = QWidget(self.centerTabEdit)
        page_layout = QGridLayout()
        page.setLayout(page_layout)
        self.centerTabEdit.addTab(page, self.textTranslate.get_txt('Home').textTranslate)

    def showTerminal(self):
        self.splitter.setSizes([self.centerTabEdit.minimumSizeHint().width(), self.terminal.sizeHint().height()])
        page = QWidget(self.terminal)
        page_layout = QGridLayout()
        page.setLayout(page_layout)
        self.terminal.addTab(page, self.textTranslate.get_txt('Terminal').textTranslate)

    def hideTerminal(self):
        self.splitter.setSizes([self.centerTabEdit.sizeHint().width(), 0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
