import enum
from typing import Optional, ClassVar
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *
import logging
import os


from dev.project.src.cl_short import IconsApp
from dev.project.src.classes.sql_server import MySQLConnection as SQLServer
from dev.project.src.classes.configurationFile import ConfigurationFile


class MainGUI(QMainWindow):

    processRunList: ClassVar[Signal] = Signal()

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)

        self.iconsManager = IconsApp(ConfigurationFile(os.getenv("ICON_FILE_RSC")))
        self.listDockWidgetManager = []

        self.loadUI()
        self.tool_uiMenu()
        self.initUI_central()


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

        self.addToolBar(Qt.LeftToolBarArea, toolsBar)
    
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
        self.v_splitter.setSizes([self.primary_center.height(), self.primary_panel.height()])

        # Splitter between Primary Side Bar and V Splitter
        self.h_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.h_splitter.addWidget(self.primary_side_bar)
        self.h_splitter.addWidget(self.v_splitter)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.h_splitter)
        self.central_widget.setLayout(layout)
