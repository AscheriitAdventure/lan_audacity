import logging, inspect
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWebEngineWidgets import QWebEngineView
from typing import Optional
from pyvis.network import Network

from src.classes.languageApp import LanguageApp


class LANMap(QWidget):
    def __init__(
            self, 
            obj_title: str,
            obj_lang: Optional[LanguageApp] = None,
            obj_view: Optional[list] = None,
            parent=None) -> None:
        super().__init__(parent)
        self.net_widget = QWebEngineView()
        self.mainLayout = QVBoxLayout()
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view
        self.netMap = Network()

        # init User Interface
        self.initUI()
        self.netMap = Network()
        self.setNetMap()

    def initUI(self):
        # Set the general layout
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        # Set the top widget
        title_widget = QWidget(self)
        self.mainLayout.addWidget(title_widget, alignment=Qt.AlignmentFlag.AlignTop)

        ttl_wdg_cnt = QHBoxLayout(title_widget)
        # Set the title
        title = QLabel(self.stackTitle)
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        ttl_wdg_cnt.addStretch()

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        self.mainLayout.addWidget(sep)

        # Set up the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.mainLayout.addWidget(scroll_area)

        # Create a widget to contain the network map
        scroll_area.setWidget(self.net_widget)
    
    def loadNetMap(self, path: Optional[str] = None):
        try:
            if path is not None:
                self.netMap.load_file(path)
                self.net_widget.setHtml(self.netMap.get_html())

        except Exception as e:
            logging.error(f"{self.__class__.__name__}::{inspect.currentframe().f_code.co_name}: Error loading the map: {e}")

    def setNetMap(self):
        self.netMap.set_options("""
            var options = {
                "physics": {
                    "forceAtlas2Based": {"springLength": 100},
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }""")
        self.netMap.show_buttons(filter_=['edges', 'nodes', 'physics'])
        self.netMap.filter_menu = True
        self.netMap.select_menu = True
    
    def editMap(self):
        # Add nodes and edges
        for item in self.objManager:
            # node = (id, label, image)
            self.netMap.add_node(item["uuid"], label=item["name"], shape='image', image=item["image"])

            # edge = (id1, id2)
            for link in item["links"]:
                self.netMap.add_edge(item["uuid"], link)
        
        # Show the map
        # retrieve the local path before showing the map
        self.netMap.show("net_map.html", open_browser=False, notebook=False)

        