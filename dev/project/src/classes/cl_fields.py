from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *
from typing import *


class NetworkField(QWidget):
    pass

    def addData(self, **kwargs) -> None:
        argl: List[tuple] = [
            ("title", str),
            ("form_list", str),
            ("icon", dict),
            ("separator", bool),
            ("collapsed", bool),
            ("actions", list),
            ("description", str),
            ("visible", bool)
        ]
        
        
        for arg in kwargs:
            pass
