from typing import Any, Optional
from enum import Enum
import os


class OSILayer(Enum):
    PHYSICAL = 1
    DATA_LINK = 2
    NETWORK = 3
    TRANSPORT = 4
    SESSION = 5
    PRESENTATION = 6
    APPLICATION = 7


class DeviceType:
    def __init__(
            self,
            ctg_nme: str,
            osi_layer: OSILayer = OSILayer.APPLICATION,
            ctg_dsc: Optional[str] = None,
            image: Optional[Any] = None,
            sub_devices: Optional[list] = None
    ):
        if not isinstance(osi_layer, OSILayer):
            raise ValueError("couche_osi doit être une instance de OSILayer")
        
        self.__pixmap = image
        self.__osi_layer = osi_layer
        self.__category_name = ctg_nme
        self.__category_description = ctg_dsc
        self.__sub_devices = sub_devices if sub_devices is not None else []

    @property
    def osiLayer(self):
        return self.__osi_layer

    @osiLayer.setter
    def osiLayer(self, osi_layer: OSILayer):
        self.__osi_layer = osi_layer
    
    @property
    def categoryName(self):
        return self.__category_name
    
    @categoryName.setter
    def categoryName(self, category_name: str):
        self.__category_name = category_name
    
    @property
    def categoryDescription(self):
        return self.__category_description
    
    @categoryDescription.setter
    def categoryDescription(self, category_description: str):
        self.__category_description = category_description
    
    @property
    def image(self):
        return self.__pixmap
    
    @image.setter
    def image(self, pixmap: Any):
        self.__pixmap = pixmap
    
    @property
    def subDevices(self):
        return self.__sub_devices
    
    @subDevices.setter
    def subDevices(self, sub_devices: list):
        self.__sub_devices = sub_devices

    def __str__(self):
        return f"DeviceType({self.__category_name}, {self.__osi_layer}, {self.__category_description}, {self.__sub_devices})"
    
    def keys(self) -> list:
        list_keys = ["Picture", "Category Name", "OSI Layer", "Category Description", "Sub-Devices"]
        if self.image is None:
            list_keys.remove("Picture")
        if self.categoryDescription is None:
            list_keys.remove("Category Description")
        if self.subDevices is None:
            list_keys.remove("Sub-Devices")
        return list_keys
    
    def jsonData(self) -> dict:
        return {
            "image": self.__pixmap,
            "ctg_nme": self.__category_name,
            "osi_layer": self.__osi_layer.name,
            "ctg_dsc": self.__category_description,
            "sub_devices": self.__sub_devices
        }
    
    def addSubDevice(self, device):
        if self.__sub_devices is None:
            self.__sub_devices = []
        self.__sub_devices.append(device)

from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtCore import QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView
from pyvis.network import Network
from pathlib import Path
import sys



class NetworkMap(QWidget):
    def __init__(self, list_obj: Optional[list]=None, parent=None) -> None:
        super().__init__(parent)
        self.netmap = Network()
        self.web_view = QWebEngineView()
        self.listObjects = list_obj if list_obj is not None else []

    
    def initUI(self):
        pass

    def editNodesMap(self, list_nodes: list):
        # Ajouter des nœuds
        for node in list_nodes:
            # node = (id, label, image)
            self.netmap.add_node(node[0], label=node[1], shape='image', image=node[2])

    def editEdgesMap(self, list_edges: list):
        # Ajouter des arêtes
        for edge in list_edges:
            # edge = (id1, id2)
            self.netmap.add_edge(edge[0], edge[1])

    def showMap(self):
        self.netmap.show("index.html", notebook=False)






print(os.getcwd())
print(os.path.join(os.getcwd(), "code", "assets", "images", "svg"))
print(OSILayer(3))