import logging
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWebEngineWidgets import QWebEngineView
from typing import Any, Optional
from pyvis.network import Network

from src.models.language_app import LanguageApp
from src.models.icons_app import IconsApp


class LANMap(QWidget):
    def __init__(
            self, 
            obj_title: str,
            obj_lang: Optional[LanguageApp]=None,
            obj_view: Optional[list]=None,
            parent=None) -> None:
        super().__init__(parent)
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager = obj_view

        # init User Interface
        self.initUI()
        self.netMap = Network()
        self.setNetMap()

    
    def initUI(self):
        # Set the general layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Set the top widget
        title_widget = QWidget(self)
        self.layout.addWidget(title_widget, alignment=Qt.AlignTop)

        ttl_wdg_cnt = QHBoxLayout(title_widget)
        # Set the title
        title = QLabel(self.stackTitle)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        ttl_wdg_cnt.addWidget(title, alignment=Qt.AlignCenter)
        ttl_wdg_cnt.addStretch()

        # set the separator
        sep = QFrame(self)
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(sep)

        # Set up the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        # Create a widget to contain the network map
        self.net_widget = QWebEngineView()
        scroll_area.setWidget(self.net_widget)
    
    def loadMap(self, path: Optional[str]=None):
        if path is not None:
            self.netMap.load_file(path)
            self.net_widget.setHtml(self.netMap.get_html())
        else:
            logging.error("No path provided to load the map")
    
    def setNetMap(self):
        self.netMap.set_options("""
            var options = {
                "physics": {
                    "forceAtlas2Based": {"springLength": 100},
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }""")
        # self.netMap.show_buttons(filter_=['edges', 'nodes', 'physics'])
        self.netMap.filter_menu = True
        # self.netMap.select_menu = True

    
    def editMap(self):
        # Add nodes and edges
        for item in self.objManager:
            # node = (id, label, image)
            self.netMap.add_node(item["uuid"], label=item["name"], shape='image', image=item["image"])

            # edge = (id1, id2)
            for link in item["links"]:
                self.netMap.add_edge(item["uuid"], link)
                

