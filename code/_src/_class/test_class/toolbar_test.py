import qtawesome as qta
import sys
from qtpy.QtWidgets import *
from qtpy.QtCore import *


class IconQta:
    def __init__(self, name: str = "Objet Non Identifié"):
        self.__icon = qta.icon("fa5s.question", color="blue")
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, var: str):
        if var != "" or var is not None:
            self.__name = var

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, var: any):
        if var is not None:
            self.__icon = var

    def __str__(self):
        return self.name


class MainBtn(QPushButton):
    def __init__(self, icon: IconQta, *args, **kwargs):
        super(MainBtn, self).__init__(*args, **kwargs)
        self.icon_obj = icon
        self.initUI()

    def initUI(self):
        self.setFixedSize(32, 32)
        self.setIconSize(self.size())
        self.setIcon(self.icon_obj.icon)


class App(QApplication):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.__title = "Lan Audacity"
        self.initUI()
        wind_icon = IconQta(name=self.windTitle)
        wind_icon.icon = qta.icon(
            "fa5s.dice-d20",
            "fa5s.spider",
            options=[
                {"color": "black"},
                {"scale_factor": 0.85, "color": "gold"},
            ],
        )
        self.window.setWindowIcon(wind_icon.icon)
        self.window.show()

    @property
    def windTitle(self):
        return self.__title

    @windTitle.setter
    def windTitle(self, var: str):
        if var != "" or var is not None:
            self.__title = var

    def set_windTitle(self, var=None):
        title = f"{self.windTitle} - {var if var else 'Untitled'}"
        self.window.setWindowTitle(title)

    def initUI(self):
        self.window = QMainWindow()  # Changed to QMainWindow

        self.set_windTitle()

        mainBar = self.window.menuBar()  # Corrected

        file_menu = mainBar.addMenu("File")
        edit_menu = mainBar.addMenu("Edit")
        help_menu = mainBar.addMenu("Help")

        # new menu item
        home_icon = IconQta(name="Accueil")
        home_icon.icon = qta.icon("fa5s.home")
        home_action = QAction(home_icon.icon, home_icon.name, self)
        home_action.setStatusTip("Ouvre la page d'accueil")
        home_action.setShortcut("Ctrl+Shift+H")
        file_menu.addAction(home_action)

        file_menu.addSeparator()

        # new open treeview: Tree Devices
        tree_icon = IconQta(name="Devices Explorer")
        tree_icon.icon = qta.icon("fa5s.atlas")
        tree_action = QAction(tree_icon.icon, tree_icon.name, self)
        tree_action.setStatusTip("Ouvre l'explorateur du réseau local")
        tree_action.setShortcut("Ctrl+Shift+G")
        file_menu.addAction(tree_action)

        # new open treeview: Tree Folder
        folder_icon = IconQta(name="Folder Explorer")
        folder_icon.icon = qta.icon("fa5s.folder", active="fa5s.folder-open")
        folder_action = QAction(folder_icon.icon, folder_icon.name, self)
        folder_action.setStatusTip("Ouvre l'explorateur de fichier")
        folder_action.setShortcut("Ctrl+Shift+E")
        file_menu.addAction(folder_action)

        # new open tab mapview: Map Devices
        map_icon = IconQta(name="Map Explorer")
        map_icon.icon = qta.icon("fa5b.hubspot")
        map_action = QAction(map_icon.icon, map_icon.name, self)
        map_action.setStatusTip("Ouvre la carte du réseau local")
        map_action.setShortcut("Ctrl+Shift+M")
        file_menu.addAction(map_action)

        # new open tab console bash: Terminal
        term_icon = IconQta(name="Terminal")
        term_icon.icon = qta.icon("fa5s.terminal")
        term_action = QAction(term_icon.icon, term_icon.name, self)
        term_action.setStatusTip("Ouvre le terminal")
        term_action.setShortcut("Ctrl+Shift+B")
        file_menu.addAction(term_action)

        file_menu.addSeparator()

        # new about tab: About
        about_icon = IconQta(name="About")
        about_icon.icon = qta.icon("fa5s.info")
        about_action = QAction(about_icon.icon, about_icon.name, self)
        about_action.setStatusTip("Ouvre la page d'information")
        about_action.setShortcut("Ctrl+Shift+I")
        help_menu.addAction(about_action)

        # toolbar
        toolbar = QToolBar("Main ToolBar")
        self.window.addToolBar(toolbar)
        toolbar.setIconSize(QSize(16, 16))

        toolbar.addAction(home_action)
        toolbar.addAction(tree_action)
        toolbar.addAction(folder_action)
        toolbar.addAction(map_action)
        toolbar.addAction(term_action)
        toolbar.addSeparator()
        toolbar.addAction(about_action)

        self.window.statusBar().showMessage("Ready")


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
