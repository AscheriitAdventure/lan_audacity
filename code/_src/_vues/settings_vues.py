from qtpy.QtCore import Qt
from qtpy.QtWidgets import *
from _src._vues.card_vues import IconCardGridView
from _src._mdl.mdl_managers import KeyboardManager, IconsManager, TextTranslateManager, SettingsModel
from _src._mdl.mdl_itm import SoftwareParameters
from _src._vues.card_vues import Card

class SettingsApp(QWidget):
    def __init__(self, obj_manager: SoftwareParameters, txt_manager: TextTranslateManager, parent=None):
        super().__init__(parent)
        self.txtManager = txt_manager
        self.objManager = obj_manager
        self.title = 'Lan Audacity'

        # Création d'un layout grid pour organiser les cartes
        appLayout = QGridLayout(self)
        widget_layout = QWidget()  # Création d'un widget pour encapsuler le grid layout
        widget_layout.setLayout(appLayout)

        # Titres du menu
        lbl_obj0 = QLabel('Software Informations')
        appLayout.addWidget(lbl_obj0, 0, 0, 1, 4)
        lbl_obj1 = QLabel('System Informations')
        appLayout.addWidget(lbl_obj1, 2, 0, 1, 4)
        lbl_obj2 = QLabel('Update Informations')
        appLayout.addWidget(lbl_obj2, 4, 0, 1, 4)

        # Cartes Objet
        card10 = Card(title=QLabel('Software Name:'), corps_card=QLineEdit(self.title))
        appLayout.addWidget(card10, 1, 0, 1, 1)

        card11 = Card(title=QLabel('Software Version:'), corps_card=QLineEdit(self.objManager.versionSftw))
        appLayout.addWidget(card11, 1, 1, 1, 1)

        card12 = Card(title=QLabel('Software Type:'), corps_card=QLineEdit(self.objManager.typeApp))
        appLayout.addWidget(card12, 1, 2, 1, 1)

        card13 = Card(title=QLabel('Website repository:'), corps_card=QLineEdit(self.objManager.updatePlatform))
        appLayout.addWidget(card13, 5, 0, 1, 1)

        card14 = Card(title=QLabel('Last Update Release:'), corps_card=QLineEdit('Unknown'))
        appLayout.addWidget(card14, 5, 1, 1, 1)

        card15 = Card(title=QLabel('Next Update Release:'), corps_card=QLineEdit('Unknown'))
        appLayout.addWidget(card15, 5, 2, 1, 1)

        card16 = Card(title=QLabel('Support Sys:'), corps_card=QLineEdit(self.objManager.osPlatform))
        appLayout.addWidget(card16, 3, 2, 1, 1)

        card17 = Card(title=QLabel('Python:'), corps_card=QLineEdit(self.objManager.pyUsed))
        appLayout.addWidget(card17, 3, 0, 1, 1)

        card18 = Card(title=QLabel('PyQt:'), corps_card=QLineEdit(self.objManager.qtUsed.upper()))
        appLayout.addWidget(card18, 3, 1, 1, 1)

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


class SettingsKeyboard(QWidget):
    def __init__(self, keyManager: KeyboardManager, txt_manager: TextTranslateManager, parent=None):
        super().__init__(parent)
        self.txtManger = txt_manager
        self.keyManager = keyManager

        menuSetLayout = QGridLayout(self)
        self.setLayout(menuSetLayout)

        # Créer une QTableWidget pour afficher les raccourcis clavier
        self.obj_view = QTableWidget(self)
        menuSetLayout.addWidget(self.obj_view, 0, 0)

        # Configurer les colonnes de la table
        self.obj_view.setColumnCount(3)
        self.obj_view.setColumnWidth(0, 200)
        self.obj_view.setColumnWidth(1, 150)
        self.obj_view.setColumnWidth(2, 150)
        self.obj_view.setHorizontalHeaderLabels(['Name Action', 'Key Shortcut', 'Icon Action'])

        # Remplir la table avec les raccourcis clavier
        for key in self.keyManager.listKeyboard:
            row = self.obj_view.rowCount()
            self.obj_view.insertRow(row)
            self.obj_view.setItem(row, 0, QTableWidgetItem(key.nameAction))
            self.obj_view.item(row, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.obj_view.setItem(row, 1, QTableWidgetItem(key.keyShortcut))
            self.obj_view.item(row, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if key.iconAction is None:
                self.obj_view.setItem(row, 2, QTableWidgetItem('Non Attribué'))
                self.obj_view.item(row, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                icon_label = QLabel(self)
                icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                icon_label.setPixmap(key.iconAction.pixmap(32, 32))
                self.obj_view.setCellWidget(row, 2, icon_label)


class SettingsIcon(QWidget):
    def __init__(self, icon_manager: IconsManager, parent=None):
        super().__init__(parent)
        self.iconManager = icon_manager

        menuSetLayout = QGridLayout(self)
        self.setLayout(menuSetLayout)

        # Créer une QTableWidget pour afficher les raccourcis clavier
        self.obj_view = QTableWidget(self)
        menuSetLayout.addWidget(self.obj_view, 0, 0)

        # Configurer les colonnes de la table
        self.obj_view.setColumnCount(2)
        self.obj_view.setColumnWidth(0, 75)
        self.obj_view.setColumnWidth(0, 200)
        self.obj_view.setHorizontalHeaderLabels(['Icon View', 'Label'])

        # Remplir la table avec les raccourcis clavier
        for ico in self.iconManager.listIcons:
            row = self.obj_view.rowCount()
            self.obj_view.insertRow(row)
            icon_label = QLabel(self, Qt.AlignmentFlag.AlignCenter)
            icon_label.setPixmap(ico.objIcon.pixmap(32, 32))
            self.obj_view.setCellWidget(row, 0, icon_label)
            self.obj_view.setItem(row, 1, QTableWidgetItem(ico.label))
            self.obj_view.item(row, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)


class SettingsMenu(QWidget):
    def __init__(self, obj_manager: SettingsModel, txt_manager: TextTranslateManager, parent=None):
        super().__init__(parent)
        self.objManager = obj_manager
        self.textTranslate = txt_manager
        self.langue = self.textTranslate.languageChoice

        self.set_ui()

    def set_ui(self):
        menuSetLayout = QGridLayout(self)
        obj_menu_vbar = QVBoxLayout(self)
        obj_menu_vbar.setContentsMargins(0, 0, 0, 0)
        obj_menu_vbar_container = QWidget(self)
        obj_menu_vbar_container.setLayout(obj_menu_vbar)
        menuSetLayout.addWidget(obj_menu_vbar_container, 0, 0, 5, 1,
                                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setLayout(menuSetLayout)

        # Extend btn
        self.extd_name = self.textTranslate.get_txt('Extends').textTranslate
        self.extend_btn = QPushButton(self.objManager.get_1_icon('extend_icon').objIcon, self.extd_name, self)
        self.extend_btn.setCheckable(True)
        self.extend_btn.icon().pixmap(48, 48)
        self.extend_btn.setToolTip(self.extd_name)
        obj_menu_vbar.addWidget(self.extend_btn)

        # Tools Home
        self.tools_name = self.textTranslate.get_txt('Application Settings').textTranslate
        self.tools_btn = QPushButton(self.objManager.get_1_icon('tools_icon').objIcon, self.tools_name, self)
        self.tools_btn.setToolTip(self.tools_name)
        self.tools_btn.icon().pixmap(48, 48)
        obj_menu_vbar.addWidget(self.tools_btn)

        # Keyboard Shortcut
        self.keyb_name = self.textTranslate.get_txt('Keyboard Shortcut').textTranslate
        self.key_short_btn = QPushButton(self.objManager.get_1_icon('key_short_icon').objIcon, self.keyb_name, self)
        self.key_short_btn.setToolTip(self.keyb_name)
        self.key_short_btn.icon().pixmap(48, 48)
        obj_menu_vbar.addWidget(self.key_short_btn)

        # Icon Used
        self.ico_name = self.textTranslate.get_txt('Icons Settings').textTranslate
        self.ico_btn = QPushButton(self.objManager.get_1_icon('ico_icon').objIcon, self.ico_name, self)
        self.ico_btn.setToolTip(self.ico_name)
        self.ico_btn.icon().pixmap(48, 48)
        obj_menu_vbar.addWidget(self.ico_btn)

        # Theme window
        self.th_wind_name = self.textTranslate.get_txt('Window Settings').textTranslate
        self.th_wind_btn = QPushButton(self.objManager.get_1_icon('th_wind_icon').objIcon, self.th_wind_name, self)
        self.th_wind_btn.setToolTip(self.th_wind_name)
        self.th_wind_btn.icon().pixmap(48, 48)
        obj_menu_vbar.addWidget(self.th_wind_btn)

        # Stacked layout pour gérer les vues changeantes
        self.stacked_layout = QStackedLayout()
        menuSetLayout.addLayout(self.stacked_layout, 1, 1, 5, 1, Qt.AlignmentFlag.AlignTop)

        # Connecter les signaux aux slots pour afficher les différentes vues
        self.extend_btn.clicked.connect(self.toggle_btns)
        self.tools_btn.clicked.connect(self.view_app_menu)
        self.key_short_btn.clicked.connect(self.view_keyboard_menu)
        self.ico_btn.clicked.connect(self.view_icon_menu)
        self.th_wind_btn.clicked.connect(self.view_window_menu)

        # Créer les vues pour chaque menu
        self.keyboard_menu = SettingsKeyboard(self.objManager.keyboard, self.textTranslate)
        self.stacked_layout.addWidget(self.keyboard_menu)
        self.icon_menu = IconCardGridView(self.objManager.icons)
        self.stacked_layout.addWidget(self.icon_menu)
        self.app_menu = SettingsApp(self.objManager.infoApp, self.textTranslate)
        self.stacked_layout.addWidget(self.app_menu)

    def toggle_btns(self):
        if self.extend_btn.isChecked():
            self.extend_btn.setText('')
            self.tools_btn.setText('')
            self.key_short_btn.setText('')
            self.ico_btn.setText('')
            self.th_wind_btn.setText('')
        else:
            self.extend_btn.setText(self.extd_name)
            self.tools_btn.setText(self.tools_name)
            self.key_short_btn.setText(self.keyb_name)
            self.ico_btn.setText(self.ico_name)
            self.th_wind_btn.setText(self.th_wind_name)

    def view_keyboard_menu(self):
        self.stacked_layout.setCurrentWidget(self.keyboard_menu)

    def view_app_menu(self):
        self.stacked_layout.setCurrentWidget(self.app_menu)

    def view_icon_menu(self):
        self.stacked_layout.setCurrentWidget(self.icon_menu)

    def view_window_menu(self):
        print('World!')
