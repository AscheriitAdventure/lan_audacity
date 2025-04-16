import logging, inspect
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWebEngineWidgets import QWebEngineView
from typing import Optional
from pyvis.network import Network

from src.classes.languageApp import LanguageApp
from src.classes.cl_network import Network as Net
import time, os


class LANMap(QWidget):
    def __init__(
            self, 
            obj_title: str,
            obj_lang: Optional[LanguageApp] = None,
            obj_view: Optional[Network] = None,
            parent=None) -> None:
        super().__init__(parent)
        self.net_widget = QWebEngineView()
        self.mainLayout = QVBoxLayout()
        self.stackTitle = obj_title
        self.langManager = obj_lang
        self.objManager: Net = obj_view
        self.netMap: Network = Network()

        # init User Interface
        self.initUI()
        self.netMap = Network()
        self.setNetMap()
        self.editMap()

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
        self.netMap.show_buttons(filter_=['edges', 'nodes', 'physics'])
        self.netMap.set_options("""
            var options = {
                "physics": {
                    "forceAtlas2Based": {"springLength": 100},
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }""")
        self.netMap.filter_menu = False
        self.netMap.select_menu = False
    
    def editMap(self):
        # Add nodes and edges
        devices = self.objManager.get_devices()
        if len(devices) > 0:
            for item in devices:
                # node = (id, label, image)
                tmp: dict = dict()
                tmp["n_id"] = item.uuid
                tmp["label"] = item.nameObj
                tmp["shape"] = "image"
                tmp["image"] = item.type.image
                # node = (id, label, image)
                self.netMap.add_node(**tmp)

                if len(item.linksList) > 0:
                # edge = (id1, id2)
                    for link in item["links"]:
                        self.netMap.add_edge(tmp["n_id"], link)
        
        # Write the map to the local file
        f_name = f"{time.time()}_graph_{self.objManager.uuid}.html"
        self.objManager.pixmaps.append(f_name)
        self.objManager.save_network()
        f_path = os.path.join(self.objManager.absPath.split(os.path.join("", "db", ""))[0], "pixmap", f_name)
        
        self.netMap.write_html(f_path)

        self.net_widget.load(QUrl.fromLocalFile(f_path))

        